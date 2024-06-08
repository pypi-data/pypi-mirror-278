# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetSnowflakeCredentialResult',
    'AwaitableGetSnowflakeCredentialResult',
    'get_snowflake_credential',
    'get_snowflake_credential_output',
]

@pulumi.output_type
class GetSnowflakeCredentialResult:
    """
    A collection of values returned by getSnowflakeCredential.
    """
    def __init__(__self__, auth_type=None, credential_id=None, id=None, is_active=None, num_threads=None, project_id=None, schema=None, user=None):
        if auth_type and not isinstance(auth_type, str):
            raise TypeError("Expected argument 'auth_type' to be a str")
        pulumi.set(__self__, "auth_type", auth_type)
        if credential_id and not isinstance(credential_id, int):
            raise TypeError("Expected argument 'credential_id' to be a int")
        pulumi.set(__self__, "credential_id", credential_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_active and not isinstance(is_active, bool):
            raise TypeError("Expected argument 'is_active' to be a bool")
        pulumi.set(__self__, "is_active", is_active)
        if num_threads and not isinstance(num_threads, int):
            raise TypeError("Expected argument 'num_threads' to be a int")
        pulumi.set(__self__, "num_threads", num_threads)
        if project_id and not isinstance(project_id, int):
            raise TypeError("Expected argument 'project_id' to be a int")
        pulumi.set(__self__, "project_id", project_id)
        if schema and not isinstance(schema, str):
            raise TypeError("Expected argument 'schema' to be a str")
        pulumi.set(__self__, "schema", schema)
        if user and not isinstance(user, str):
            raise TypeError("Expected argument 'user' to be a str")
        pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter(name="authType")
    def auth_type(self) -> str:
        """
        The type of Snowflake credential ('password' or 'keypair')
        """
        return pulumi.get(self, "auth_type")

    @property
    @pulumi.getter(name="credentialId")
    def credential_id(self) -> int:
        """
        Credential ID
        """
        return pulumi.get(self, "credential_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isActive")
    def is_active(self) -> bool:
        """
        Whether the Snowflake credential is active
        """
        return pulumi.get(self, "is_active")

    @property
    @pulumi.getter(name="numThreads")
    def num_threads(self) -> int:
        """
        Number of threads to use
        """
        return pulumi.get(self, "num_threads")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> int:
        """
        Project ID
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def schema(self) -> str:
        """
        Default schema name
        """
        return pulumi.get(self, "schema")

    @property
    @pulumi.getter
    def user(self) -> str:
        """
        Username for Snowflake
        """
        return pulumi.get(self, "user")


class AwaitableGetSnowflakeCredentialResult(GetSnowflakeCredentialResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSnowflakeCredentialResult(
            auth_type=self.auth_type,
            credential_id=self.credential_id,
            id=self.id,
            is_active=self.is_active,
            num_threads=self.num_threads,
            project_id=self.project_id,
            schema=self.schema,
            user=self.user)


def get_snowflake_credential(credential_id: Optional[int] = None,
                             project_id: Optional[int] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSnowflakeCredentialResult:
    """
    Use this data source to access information about an existing resource.

    :param int credential_id: Credential ID
    :param int project_id: Project ID
    """
    __args__ = dict()
    __args__['credentialId'] = credential_id
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('dbtcloud:index/getSnowflakeCredential:getSnowflakeCredential', __args__, opts=opts, typ=GetSnowflakeCredentialResult).value

    return AwaitableGetSnowflakeCredentialResult(
        auth_type=pulumi.get(__ret__, 'auth_type'),
        credential_id=pulumi.get(__ret__, 'credential_id'),
        id=pulumi.get(__ret__, 'id'),
        is_active=pulumi.get(__ret__, 'is_active'),
        num_threads=pulumi.get(__ret__, 'num_threads'),
        project_id=pulumi.get(__ret__, 'project_id'),
        schema=pulumi.get(__ret__, 'schema'),
        user=pulumi.get(__ret__, 'user'))


@_utilities.lift_output_func(get_snowflake_credential)
def get_snowflake_credential_output(credential_id: Optional[pulumi.Input[int]] = None,
                                    project_id: Optional[pulumi.Input[int]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSnowflakeCredentialResult]:
    """
    Use this data source to access information about an existing resource.

    :param int credential_id: Credential ID
    :param int project_id: Project ID
    """
    ...
