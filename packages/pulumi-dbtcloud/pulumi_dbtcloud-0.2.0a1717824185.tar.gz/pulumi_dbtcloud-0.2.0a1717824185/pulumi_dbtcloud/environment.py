# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['EnvironmentArgs', 'Environment']

@pulumi.input_type
class EnvironmentArgs:
    def __init__(__self__, *,
                 dbt_version: pulumi.Input[str],
                 project_id: pulumi.Input[int],
                 type: pulumi.Input[str],
                 credential_id: Optional[pulumi.Input[int]] = None,
                 custom_branch: Optional[pulumi.Input[str]] = None,
                 deployment_type: Optional[pulumi.Input[str]] = None,
                 extended_attributes_id: Optional[pulumi.Input[int]] = None,
                 is_active: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 use_custom_branch: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Environment resource.
        :param pulumi.Input[str] dbt_version: Version number of dbt to use in this environment. It needs to be in the format `major.minor.0-latest` (e.g. `1.5.0-latest`), `major.minor.0-pre` or `versionless`. In a future version of the provider `versionless` will be the default if no version is provided
        :param pulumi.Input[int] project_id: Project ID to create the environment in
        :param pulumi.Input[str] type: The type of environment (must be either development or deployment)
        :param pulumi.Input[int] credential_id: Credential ID to create the environment with. A credential is not required for development environments but is required for deployment environments
        :param pulumi.Input[str] custom_branch: Which custom branch to use in this environment
        :param pulumi.Input[str] deployment_type: The type of environment. Only valid for environments of type 'deployment' and for now can only be empty or set to 'production'
        :param pulumi.Input[int] extended_attributes_id: ID of the extended attributes for the environment
        :param pulumi.Input[bool] is_active: Whether the environment is active
        :param pulumi.Input[str] name: Environment name
        :param pulumi.Input[bool] use_custom_branch: Whether to use a custom git branch in this environment
        """
        pulumi.set(__self__, "dbt_version", dbt_version)
        pulumi.set(__self__, "project_id", project_id)
        pulumi.set(__self__, "type", type)
        if credential_id is not None:
            pulumi.set(__self__, "credential_id", credential_id)
        if custom_branch is not None:
            pulumi.set(__self__, "custom_branch", custom_branch)
        if deployment_type is not None:
            pulumi.set(__self__, "deployment_type", deployment_type)
        if extended_attributes_id is not None:
            pulumi.set(__self__, "extended_attributes_id", extended_attributes_id)
        if is_active is not None:
            pulumi.set(__self__, "is_active", is_active)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if use_custom_branch is not None:
            pulumi.set(__self__, "use_custom_branch", use_custom_branch)

    @property
    @pulumi.getter(name="dbtVersion")
    def dbt_version(self) -> pulumi.Input[str]:
        """
        Version number of dbt to use in this environment. It needs to be in the format `major.minor.0-latest` (e.g. `1.5.0-latest`), `major.minor.0-pre` or `versionless`. In a future version of the provider `versionless` will be the default if no version is provided
        """
        return pulumi.get(self, "dbt_version")

    @dbt_version.setter
    def dbt_version(self, value: pulumi.Input[str]):
        pulumi.set(self, "dbt_version", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Input[int]:
        """
        Project ID to create the environment in
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: pulumi.Input[int]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of environment (must be either development or deployment)
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="credentialId")
    def credential_id(self) -> Optional[pulumi.Input[int]]:
        """
        Credential ID to create the environment with. A credential is not required for development environments but is required for deployment environments
        """
        return pulumi.get(self, "credential_id")

    @credential_id.setter
    def credential_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "credential_id", value)

    @property
    @pulumi.getter(name="customBranch")
    def custom_branch(self) -> Optional[pulumi.Input[str]]:
        """
        Which custom branch to use in this environment
        """
        return pulumi.get(self, "custom_branch")

    @custom_branch.setter
    def custom_branch(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_branch", value)

    @property
    @pulumi.getter(name="deploymentType")
    def deployment_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of environment. Only valid for environments of type 'deployment' and for now can only be empty or set to 'production'
        """
        return pulumi.get(self, "deployment_type")

    @deployment_type.setter
    def deployment_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "deployment_type", value)

    @property
    @pulumi.getter(name="extendedAttributesId")
    def extended_attributes_id(self) -> Optional[pulumi.Input[int]]:
        """
        ID of the extended attributes for the environment
        """
        return pulumi.get(self, "extended_attributes_id")

    @extended_attributes_id.setter
    def extended_attributes_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "extended_attributes_id", value)

    @property
    @pulumi.getter(name="isActive")
    def is_active(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the environment is active
        """
        return pulumi.get(self, "is_active")

    @is_active.setter
    def is_active(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_active", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Environment name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="useCustomBranch")
    def use_custom_branch(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to use a custom git branch in this environment
        """
        return pulumi.get(self, "use_custom_branch")

    @use_custom_branch.setter
    def use_custom_branch(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_custom_branch", value)


@pulumi.input_type
class _EnvironmentState:
    def __init__(__self__, *,
                 credential_id: Optional[pulumi.Input[int]] = None,
                 custom_branch: Optional[pulumi.Input[str]] = None,
                 dbt_version: Optional[pulumi.Input[str]] = None,
                 deployment_type: Optional[pulumi.Input[str]] = None,
                 environment_id: Optional[pulumi.Input[int]] = None,
                 extended_attributes_id: Optional[pulumi.Input[int]] = None,
                 is_active: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 use_custom_branch: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering Environment resources.
        :param pulumi.Input[int] credential_id: Credential ID to create the environment with. A credential is not required for development environments but is required for deployment environments
        :param pulumi.Input[str] custom_branch: Which custom branch to use in this environment
        :param pulumi.Input[str] dbt_version: Version number of dbt to use in this environment. It needs to be in the format `major.minor.0-latest` (e.g. `1.5.0-latest`), `major.minor.0-pre` or `versionless`. In a future version of the provider `versionless` will be the default if no version is provided
        :param pulumi.Input[str] deployment_type: The type of environment. Only valid for environments of type 'deployment' and for now can only be empty or set to 'production'
        :param pulumi.Input[int] environment_id: Environment ID within the project
        :param pulumi.Input[int] extended_attributes_id: ID of the extended attributes for the environment
        :param pulumi.Input[bool] is_active: Whether the environment is active
        :param pulumi.Input[str] name: Environment name
        :param pulumi.Input[int] project_id: Project ID to create the environment in
        :param pulumi.Input[str] type: The type of environment (must be either development or deployment)
        :param pulumi.Input[bool] use_custom_branch: Whether to use a custom git branch in this environment
        """
        if credential_id is not None:
            pulumi.set(__self__, "credential_id", credential_id)
        if custom_branch is not None:
            pulumi.set(__self__, "custom_branch", custom_branch)
        if dbt_version is not None:
            pulumi.set(__self__, "dbt_version", dbt_version)
        if deployment_type is not None:
            pulumi.set(__self__, "deployment_type", deployment_type)
        if environment_id is not None:
            pulumi.set(__self__, "environment_id", environment_id)
        if extended_attributes_id is not None:
            pulumi.set(__self__, "extended_attributes_id", extended_attributes_id)
        if is_active is not None:
            pulumi.set(__self__, "is_active", is_active)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if use_custom_branch is not None:
            pulumi.set(__self__, "use_custom_branch", use_custom_branch)

    @property
    @pulumi.getter(name="credentialId")
    def credential_id(self) -> Optional[pulumi.Input[int]]:
        """
        Credential ID to create the environment with. A credential is not required for development environments but is required for deployment environments
        """
        return pulumi.get(self, "credential_id")

    @credential_id.setter
    def credential_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "credential_id", value)

    @property
    @pulumi.getter(name="customBranch")
    def custom_branch(self) -> Optional[pulumi.Input[str]]:
        """
        Which custom branch to use in this environment
        """
        return pulumi.get(self, "custom_branch")

    @custom_branch.setter
    def custom_branch(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_branch", value)

    @property
    @pulumi.getter(name="dbtVersion")
    def dbt_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version number of dbt to use in this environment. It needs to be in the format `major.minor.0-latest` (e.g. `1.5.0-latest`), `major.minor.0-pre` or `versionless`. In a future version of the provider `versionless` will be the default if no version is provided
        """
        return pulumi.get(self, "dbt_version")

    @dbt_version.setter
    def dbt_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dbt_version", value)

    @property
    @pulumi.getter(name="deploymentType")
    def deployment_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of environment. Only valid for environments of type 'deployment' and for now can only be empty or set to 'production'
        """
        return pulumi.get(self, "deployment_type")

    @deployment_type.setter
    def deployment_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "deployment_type", value)

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> Optional[pulumi.Input[int]]:
        """
        Environment ID within the project
        """
        return pulumi.get(self, "environment_id")

    @environment_id.setter
    def environment_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "environment_id", value)

    @property
    @pulumi.getter(name="extendedAttributesId")
    def extended_attributes_id(self) -> Optional[pulumi.Input[int]]:
        """
        ID of the extended attributes for the environment
        """
        return pulumi.get(self, "extended_attributes_id")

    @extended_attributes_id.setter
    def extended_attributes_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "extended_attributes_id", value)

    @property
    @pulumi.getter(name="isActive")
    def is_active(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the environment is active
        """
        return pulumi.get(self, "is_active")

    @is_active.setter
    def is_active(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_active", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Environment name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[int]]:
        """
        Project ID to create the environment in
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of environment (must be either development or deployment)
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="useCustomBranch")
    def use_custom_branch(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to use a custom git branch in this environment
        """
        return pulumi.get(self, "use_custom_branch")

    @use_custom_branch.setter
    def use_custom_branch(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_custom_branch", value)


class Environment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 credential_id: Optional[pulumi.Input[int]] = None,
                 custom_branch: Optional[pulumi.Input[str]] = None,
                 dbt_version: Optional[pulumi.Input[str]] = None,
                 deployment_type: Optional[pulumi.Input[str]] = None,
                 extended_attributes_id: Optional[pulumi.Input[int]] = None,
                 is_active: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 use_custom_branch: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_dbtcloud as dbtcloud

        ci_environment = dbtcloud.Environment("ci_environment",
            dbt_version="versionless",
            name="CI",
            project_id=dbt_project["id"],
            type="deployment",
            credential_id=ci_credential["credentialId"])
        # we can also set a deployment environment as being the production one
        prod_environment = dbtcloud.Environment("prod_environment",
            dbt_version="1.7.0-latest",
            name="Prod",
            project_id=dbt_project["id"],
            type="deployment",
            credential_id=prod_credential["credentialId"],
            deployment_type="production")
        # Creating a development environment
        dev_environment = dbtcloud.Environment("dev_environment",
            dbt_version="versionless",
            name="Dev",
            project_id=dbt_project["id"],
            type="development")
        ```

        ## Import

        using  import blocks (requires Terraform >= 1.5)

        import {

          to = dbtcloud_environment.prod_environment

          id = "project_id:environment_id"

        }

        import {

          to = dbtcloud_environment.prod_environment

          id = "12345:6789"

        }

        using the older import command

        ```sh
        $ pulumi import dbtcloud:index/environment:Environment prod_environment "project_id:environment_id"
        ```

        ```sh
        $ pulumi import dbtcloud:index/environment:Environment prod_environment 12345:6789
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] credential_id: Credential ID to create the environment with. A credential is not required for development environments but is required for deployment environments
        :param pulumi.Input[str] custom_branch: Which custom branch to use in this environment
        :param pulumi.Input[str] dbt_version: Version number of dbt to use in this environment. It needs to be in the format `major.minor.0-latest` (e.g. `1.5.0-latest`), `major.minor.0-pre` or `versionless`. In a future version of the provider `versionless` will be the default if no version is provided
        :param pulumi.Input[str] deployment_type: The type of environment. Only valid for environments of type 'deployment' and for now can only be empty or set to 'production'
        :param pulumi.Input[int] extended_attributes_id: ID of the extended attributes for the environment
        :param pulumi.Input[bool] is_active: Whether the environment is active
        :param pulumi.Input[str] name: Environment name
        :param pulumi.Input[int] project_id: Project ID to create the environment in
        :param pulumi.Input[str] type: The type of environment (must be either development or deployment)
        :param pulumi.Input[bool] use_custom_branch: Whether to use a custom git branch in this environment
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EnvironmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_dbtcloud as dbtcloud

        ci_environment = dbtcloud.Environment("ci_environment",
            dbt_version="versionless",
            name="CI",
            project_id=dbt_project["id"],
            type="deployment",
            credential_id=ci_credential["credentialId"])
        # we can also set a deployment environment as being the production one
        prod_environment = dbtcloud.Environment("prod_environment",
            dbt_version="1.7.0-latest",
            name="Prod",
            project_id=dbt_project["id"],
            type="deployment",
            credential_id=prod_credential["credentialId"],
            deployment_type="production")
        # Creating a development environment
        dev_environment = dbtcloud.Environment("dev_environment",
            dbt_version="versionless",
            name="Dev",
            project_id=dbt_project["id"],
            type="development")
        ```

        ## Import

        using  import blocks (requires Terraform >= 1.5)

        import {

          to = dbtcloud_environment.prod_environment

          id = "project_id:environment_id"

        }

        import {

          to = dbtcloud_environment.prod_environment

          id = "12345:6789"

        }

        using the older import command

        ```sh
        $ pulumi import dbtcloud:index/environment:Environment prod_environment "project_id:environment_id"
        ```

        ```sh
        $ pulumi import dbtcloud:index/environment:Environment prod_environment 12345:6789
        ```

        :param str resource_name: The name of the resource.
        :param EnvironmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnvironmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 credential_id: Optional[pulumi.Input[int]] = None,
                 custom_branch: Optional[pulumi.Input[str]] = None,
                 dbt_version: Optional[pulumi.Input[str]] = None,
                 deployment_type: Optional[pulumi.Input[str]] = None,
                 extended_attributes_id: Optional[pulumi.Input[int]] = None,
                 is_active: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 use_custom_branch: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EnvironmentArgs.__new__(EnvironmentArgs)

            __props__.__dict__["credential_id"] = credential_id
            __props__.__dict__["custom_branch"] = custom_branch
            if dbt_version is None and not opts.urn:
                raise TypeError("Missing required property 'dbt_version'")
            __props__.__dict__["dbt_version"] = dbt_version
            __props__.__dict__["deployment_type"] = deployment_type
            __props__.__dict__["extended_attributes_id"] = extended_attributes_id
            __props__.__dict__["is_active"] = is_active
            __props__.__dict__["name"] = name
            if project_id is None and not opts.urn:
                raise TypeError("Missing required property 'project_id'")
            __props__.__dict__["project_id"] = project_id
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["use_custom_branch"] = use_custom_branch
            __props__.__dict__["environment_id"] = None
        super(Environment, __self__).__init__(
            'dbtcloud:index/environment:Environment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            credential_id: Optional[pulumi.Input[int]] = None,
            custom_branch: Optional[pulumi.Input[str]] = None,
            dbt_version: Optional[pulumi.Input[str]] = None,
            deployment_type: Optional[pulumi.Input[str]] = None,
            environment_id: Optional[pulumi.Input[int]] = None,
            extended_attributes_id: Optional[pulumi.Input[int]] = None,
            is_active: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[int]] = None,
            type: Optional[pulumi.Input[str]] = None,
            use_custom_branch: Optional[pulumi.Input[bool]] = None) -> 'Environment':
        """
        Get an existing Environment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] credential_id: Credential ID to create the environment with. A credential is not required for development environments but is required for deployment environments
        :param pulumi.Input[str] custom_branch: Which custom branch to use in this environment
        :param pulumi.Input[str] dbt_version: Version number of dbt to use in this environment. It needs to be in the format `major.minor.0-latest` (e.g. `1.5.0-latest`), `major.minor.0-pre` or `versionless`. In a future version of the provider `versionless` will be the default if no version is provided
        :param pulumi.Input[str] deployment_type: The type of environment. Only valid for environments of type 'deployment' and for now can only be empty or set to 'production'
        :param pulumi.Input[int] environment_id: Environment ID within the project
        :param pulumi.Input[int] extended_attributes_id: ID of the extended attributes for the environment
        :param pulumi.Input[bool] is_active: Whether the environment is active
        :param pulumi.Input[str] name: Environment name
        :param pulumi.Input[int] project_id: Project ID to create the environment in
        :param pulumi.Input[str] type: The type of environment (must be either development or deployment)
        :param pulumi.Input[bool] use_custom_branch: Whether to use a custom git branch in this environment
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EnvironmentState.__new__(_EnvironmentState)

        __props__.__dict__["credential_id"] = credential_id
        __props__.__dict__["custom_branch"] = custom_branch
        __props__.__dict__["dbt_version"] = dbt_version
        __props__.__dict__["deployment_type"] = deployment_type
        __props__.__dict__["environment_id"] = environment_id
        __props__.__dict__["extended_attributes_id"] = extended_attributes_id
        __props__.__dict__["is_active"] = is_active
        __props__.__dict__["name"] = name
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["type"] = type
        __props__.__dict__["use_custom_branch"] = use_custom_branch
        return Environment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="credentialId")
    def credential_id(self) -> pulumi.Output[Optional[int]]:
        """
        Credential ID to create the environment with. A credential is not required for development environments but is required for deployment environments
        """
        return pulumi.get(self, "credential_id")

    @property
    @pulumi.getter(name="customBranch")
    def custom_branch(self) -> pulumi.Output[Optional[str]]:
        """
        Which custom branch to use in this environment
        """
        return pulumi.get(self, "custom_branch")

    @property
    @pulumi.getter(name="dbtVersion")
    def dbt_version(self) -> pulumi.Output[str]:
        """
        Version number of dbt to use in this environment. It needs to be in the format `major.minor.0-latest` (e.g. `1.5.0-latest`), `major.minor.0-pre` or `versionless`. In a future version of the provider `versionless` will be the default if no version is provided
        """
        return pulumi.get(self, "dbt_version")

    @property
    @pulumi.getter(name="deploymentType")
    def deployment_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of environment. Only valid for environments of type 'deployment' and for now can only be empty or set to 'production'
        """
        return pulumi.get(self, "deployment_type")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> pulumi.Output[int]:
        """
        Environment ID within the project
        """
        return pulumi.get(self, "environment_id")

    @property
    @pulumi.getter(name="extendedAttributesId")
    def extended_attributes_id(self) -> pulumi.Output[Optional[int]]:
        """
        ID of the extended attributes for the environment
        """
        return pulumi.get(self, "extended_attributes_id")

    @property
    @pulumi.getter(name="isActive")
    def is_active(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether the environment is active
        """
        return pulumi.get(self, "is_active")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Environment name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[int]:
        """
        Project ID to create the environment in
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of environment (must be either development or deployment)
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="useCustomBranch")
    def use_custom_branch(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to use a custom git branch in this environment
        """
        return pulumi.get(self, "use_custom_branch")

