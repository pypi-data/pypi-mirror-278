"""
ECR Scan information
"""

from pathlib import Path
from typing import List, Optional

from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import get_current_datetime, is_valid_fqdn
from regscale.models.integration_models.container_scan import ContainerScan
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.issue import Issue
from regscale.models.regscale_models.vulnerability import Vulnerability


class ECR(ContainerScan):
    """ECR Scan information"""

    def __init__(self, name: str, app: Application, **kwargs):
        self.name = name
        self.vuln_title = "name"
        self.fmt = "%m/%d/%y"
        self.dt_format = "%Y-%m-%d %H:%M:%S"
        self.image_name = "Name"
        self.headers = [
            "Name",
            "Tag",
            "Severity",
            "CVE",
            "Description",
            "Package Name",
            "Package Version",
            "CVSS2 Score",
            "CVSS2 Vector",
            "URI",
        ]

        file_path = kwargs.get("file_path")
        parent_id = kwargs.get("parent_id")
        parent_module = kwargs.get("parent_module")
        logger = create_logger()
        super().__init__(
            logger=logger,
            app=app,
            file_path=Path(file_path),
            name=self.name.lower(),
            headers=self.headers,
            parent_id=parent_id,
            parent_module=parent_module,
            file_type=".json",
            asset_func=self.create_asset,
            vuln_func=self.create_vuln,
            issue_func=self.create_issue,
        )

    def create_issue(self, **kwargs: dict) -> Optional[List[Issue]]:
        """
        Create an issue from a row in the ECR file

        :param dict **kwargs: The keyword arguments for this function
        :return: RegScale Issue object or None
        :rtype: Optional[List[Issue]]
        """
        issues: List[Issue] = []
        dat = kwargs.get("dat", {})
        findings = dat.get("imageScanFindings").get("findings")
        repository_name = dat.get("repositoryName", "")
        image_id_data = dat.get("imageId", {}).get("imageDigest", "").split(":")
        if len(image_id_data) > 1:
            image_id = image_id_data[1]
        else:
            image_id = image_id_data[0]
        name = f"{repository_name}:{image_id}"
        if findings:
            for finding in findings:
                severity = self.determine_severity(finding.get("severity", ""))  # "" will return info
                if severity == "info":
                    return None
                dt_first_detected = self.scan_date
                iss = super().create_issue(
                    dat=finding,
                    severity=severity,
                    first_detected_dt=dt_first_detected,
                    description=finding.get("uri", ""),
                    asset_identifier=name,
                )
                if iss:
                    issues.append(iss)
        return issues

    def create_asset(self, dat: Optional[dict] = None) -> Asset:
        """
        Create an asset from a row in the ECR file

        :param Optional[dict] dat: Data row from file, defaults to None
        :return: RegScale Asset object
        :rtype: Asset
        """
        repository_name = dat.get("repositoryName", "")
        image_id_data = dat.get("imageId", {}).get("imageDigest", "").split(":")
        if len(image_id_data) > 1:
            image_id = image_id_data[1]
        else:
            image_id = image_id_data[0]
        name = f"{repository_name}:{image_id}"
        # Check if string has a forward slash
        return Asset(
            **{
                "id": 0,
                "name": name,
                "description": "Container Image" if "/" in name else "",
                "operatingSystem": "Linux",
                "operatingSystemVersion": "",
                "ipAddress": "0.0.0.0",
                "isPublic": True,
                "status": "Active (On Network)",
                "assetCategory": "Software",
                "bLatestScan": True,
                "bAuthenticatedScan": True,
                "scanningTool": self.name,
                "assetOwnerId": self.config["userId"],
                "assetType": "Other",
                "fqdn": name if is_valid_fqdn(name) else None,
                "systemAdministratorId": self.config["userId"],
                "parentId": self.attributes.parent_id,
                "parentModule": self.attributes.parent_module,
            }
        )

    def create_vuln(self, dat: Optional[dict] = None) -> Optional[List[Vulnerability]]:
        """
        Create a vulnerability from a row in the ECR csv file

        :param Optional[dict] dat: Data row from file, defaults to None
        :return: RegScale Vulnerability object or None
        :rtype: Optional[List[Vulnerability]]
        """
        repository_name = dat.get("repositoryName", "")
        image_id_data = dat.get("imageId", {}).get("imageDigest", "").split(":")
        if len(image_id_data) > 1:
            image_id = image_id_data[1]
        else:
            image_id = image_id_data[0]
        hostname = f"{repository_name}:{image_id}"
        vulns: List[Vulnerability] = []
        regscale_vuln = None
        findings = dat.get("imageScanFindings").get("findings")
        if findings:
            for finding in findings:
                cve = finding.get("name")
                severity = self.determine_severity(finding["severity"])
                config = self.attributes.app.config
                asset_match = [asset for asset in self.data["assets"] if asset.name == hostname]
                asset = asset_match[0] if asset_match else None
                if asset_match:
                    regscale_vuln = Vulnerability(
                        id=0,
                        scanId=0,
                        parentId=asset.id,
                        parentModule="assets",
                        ipAddress="0.0.0.0",
                        lastSeen=get_current_datetime(),  # No timestamp on ECR
                        # firstSeen=get_current_datetime(), # No timestamp on ECR
                        daysOpen=None,
                        dns=hostname,
                        mitigated=None,
                        operatingSystem=asset.operatingSystem,
                        severity=severity,
                        plugInName=cve,
                        cve=cve,
                        tenantsId=0,
                        title=f"{cve} on asset {asset.name}",
                        description=cve,
                        plugInText=finding.get("uri", ""),
                        createdById=config["userId"],
                        lastUpdatedById=config["userId"],
                        dateCreated=get_current_datetime(),
                    )
                    vulns.append(regscale_vuln)
        return vulns

    @staticmethod
    def determine_severity(s: str) -> str:
        """
        Determine the CVSS severity of the vulnerability

        :param str s: The severity
        :return: The severity
        :rtype: str
        """
        severity = "info"
        if s:
            severity = s.lower()
        # remap crits to highs
        if severity == "critical":
            severity = "high"
        return severity
