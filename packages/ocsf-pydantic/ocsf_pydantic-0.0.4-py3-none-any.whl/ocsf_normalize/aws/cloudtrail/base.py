from ocsf.events.application.api import APIActivity, APIActivityId
from ocsf.events.base import SeverityID
from ocsf.objects.account import Account
from ocsf.objects.actor import Actor
from ocsf.objects.api import API
from ocsf.objects.cloud import Cloud
from ocsf.objects.http_request import HTTPRequest
from ocsf.objects.metadata import Metadata
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.product import Feature, Product
from ocsf.objects.resource_details import ResourceDetails
from ocsf.objects.service import Service
from ocsf.objects.session import Session
from ocsf.objects.user import User


class Cloudtrail(APIActivity):
    def __init__(self, data: dict, correlation_id: str | None = None):
        metadata = Metadata(correlation_uid=correlation_id,
                            product=Product(vendor_name='AWS',
                                            name='CloudTrail',
                                            feature=Feature(name=data.get('eventCategory')),
                                            version=data.get('eventVersion')),
                            uid=data.get('eventId'),
                            event_code=data.get('eventType'),
                            profiles=['cloud'])

        useridentity: dict = data.get('userIdentity', {})
        sessiondata: dict = useridentity.get('sessionContext')

        if sessiondata:
            iss: dict = sessiondata.get('sessionIssuer', {})
            attr: dict = sessiondata.get('attributes', {})
            session=Session(issuer=iss.get('arn'),
                            created_time=attr.get('creationDate'),
                            is_mfa=attr.get('mfaAuthenticated'))
        else:
            session = None

        pid: str = useridentity.get('principalId')
        email: str | None = pid.split(':')[-1] if pid and '@' in pid else None

        actor = Actor(user=User(account=Account(uid=useridentity.get('accountId')),
                                type=useridentity.get('type'),
                                uid=useridentity.get('arn'),
                                uid_alt=useridentity.get('principalId'),
                                credential_uid=useridentity.get('accessKeyId'),
                                email_addr=email),
                      session=session)

        if data.get('sourceIPAddress', '').endswith('.amazonaws.com') or \
                data.get('sourceIPAddress') == 'AWS Internal':
            src_endpoint=NetworkEndpoint(domain=data.get('sourceIPAddress'))
        else:
            src_endpoint=NetworkEndpoint(ip_address=data.get('sourceIPAddress'))

        resources = []
        for resource in data.get('resources', []):
            uid = resource.get('ARN')
            acct = resource.get('accountId')
            owner = User(account=Account(uid=acct)) if acct else None
            if uid and owner:
                resources.append(ResourceDetails(uid=uid,
                                                 owner=owner,
                                                 type=resource.get('type')))
        super().__init__(metadata=metadata,
                         api = API(operation=data.get('eventName'),
                                   service=Service(name=data.get('eventSource'))),
                         cloud = Cloud(provider='AWS',
                                       region=data.get('awsRegion')),
                         actor=actor,
                         activity_id=APIActivityId.Other,
                         activity_name=data.get('eventName'),
                         severity_id=SeverityID.Informational,
                         src_endpoint=src_endpoint,
                         http_request=HTTPRequest(user_agent=data.get('userAgent')),
                         resources=resources if len(resources) > 0 else None,
                         time=data.get('eventTime'))
