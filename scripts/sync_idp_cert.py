"""Copy the Keycloak realm signing certificate into both service providers.

Keycloak generates a fresh RSA key pair for the realm the first time it
imports keycloak/realm-export.json, so no private key ever lives in this
repository. The service providers still need the matching public certificate
to verify signed SAML assertions; this script fetches it from the realm's
SAML descriptor and writes it to each SP's saml/settings.json, along with a
copy of the IdP metadata.

Run it once after `docker compose up`, when Keycloak is reachable:

    python scripts/sync_idp_cert.py
"""

from __future__ import annotations

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

DESCRIPTOR_URL = "http://localhost:8080/realms/gid-dev/protocol/saml/descriptor"
ROOT = Path(__file__).resolve().parent.parent
SP_DIRS = [ROOT / "backend" / "saml", ROOT / "backend2" / "saml"]
NS = {
    "md": "urn:oasis:names:tc:SAML:2.0:metadata",
    "ds": "http://www.w3.org/2000/09/xmldsig#",
}


def signing_certificate(metadata_xml: str) -> str:
    """Return the base64 signing certificate from SAML IdP metadata."""
    root = ET.fromstring(metadata_xml)
    for descriptor in root.iterfind(".//md:KeyDescriptor", NS):
        if descriptor.get("use") in (None, "signing"):
            cert = descriptor.find(".//ds:X509Certificate", NS)
            if cert is not None and cert.text:
                return "".join(cert.text.split())
    raise ValueError("no signing certificate found in IdP metadata")


def main() -> int:
    try:
        with urllib.request.urlopen(DESCRIPTOR_URL, timeout=10) as resp:
            metadata = resp.read().decode()
    except OSError as exc:
        print(f"Could not reach Keycloak at {DESCRIPTOR_URL}: {exc}", file=sys.stderr)
        return 1

    cert = signing_certificate(metadata)
    for sp_dir in SP_DIRS:
        settings_path = sp_dir / "settings.json"
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        settings["idp"]["x509cert"] = cert
        settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
        (sp_dir / "idp_metadata.xml").write_text(metadata, encoding="utf-8")
        print(f"Updated {settings_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
