'''
# DMS Patterns - a library to facilitate migrations

This library aims at simplifying the task of setting up a migration project using AWS DMS and the AWS CDK, by providing L2 constructs that take care of creating the necessary roles and resources and high-level L3 constructs that represent migration patterns from a database (in the cloud or a DB in AWS RDS) to AWS s3. See the example section below for more details.

This library is  written using the wonderful [projen](https://github.com/projen/projen) framework.

Note: this library is just the result of some personal experimentation. It is not an official AWS library and is not supported by AWS!

# Installation

The library is available on npmjs.com and can be installed using:

`npm i dms-patterns`

And on pypi:

`pip install dms-patterns`

# Usage Examples

## Deploying the dms-vpc-role

If you use the AWS CLI or the AWS DMS API for your database migration, you must add three IAM roles to your AWS account before you can use the features of AWS DMS (see [here](https://docs.aws.amazon.com/dms/latest/userguide/security-iam.html#CHAP_Security.APIRole)).

The dms-patterns includes a stack that creates these roles for you. Here is an example of how to use it:

```python
import { DmsVpcRoleStack } from 'dms-patterns';

const app = new cdk.App();
new DmsVpcRoleStack(app, 'DmsVpcRoleStack');
```

adding an explicit dependency might be required to make sure that the role is deployed prior to the migration stack.

## Migrating data from MySQL to S3

This section demonstrates creating a stack that migrates data from a MySQL database to S3. The stack is created in TypeScript, but the same constructs are available in Python.
We start by adding a source endpoint to our stack:

```python
this.source = new MySqlEndpoint(this, 'SourceEndpoint', {
  endpointType: EndpointType.SOURCE,
  databaseName: *******,
  endpointIdentifier: 'mysqlEndpoint',
  mySqlEndpointSettings: {
    secretsManagerSecretId: 'arn:aws:secretsmanager:**********',
 },
});
```

A MySqlEndpoint is just a [dms.CfnEndpoint](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html), but the construct also takes care of initializing a secretsManagerAccessRole used by DMS to read the specified secret, that contains the necessary connection details:

```json
{
  "password":"*****",
  "username":"*****",
  "port":3306,
  "host":"****"
}
```

Our target is :

```python
this.target = new S3TargetEndpoint(this, 'S3Target', {
  bucketArn: props.bucketArn,
});
```

the construct takes again care of creating the necessary role for creating objects within the given bucket.

We can now define the replication itself. In case no default (subnet) vpc exists in your account, you may want to create a replicationSubnetGroup that describes where your resources will be deployed:

```python
const replicationSubnetGroup = new dms.CfnReplicationSubnetGroup(this, 'ReplicationSubnetGroup', {
  replicationSubnetGroupDescription: 'ReplicationSubnetGroup',
  replicationSubnetGroupIdentifier: 'mysqlreplicationsubnetID',
  subnetIds: [
    'subnet-******',
    'subnet-******',
    'subnet-******',
  ],
});
```

and, finally, a computeConfig:

```python
const computeConfig: dms.CfnReplicationConfig.ComputeConfigProperty = {
  minCapacityUnits: CapacityUnits._1,
  maxCapacityUnits: CapacityUnits._2,
  multiAz: false,
  replicationSubnetGroupId: replicationSubnetGroup.replicationSubnetGroupIdentifier,
  vpcSecurityGroupIds: [
    replicationSecurityGroup.securityGroupId,
  ],
};
```

and some rules for e.g. selecting the right tables:

```python
    const tableMappings = new TableMappings(
      [
        new SelectionRule(
          {
            objectLocator: {
              schemaName: 'schemaname',
              tableName: 'tableName',
            },
            ruleAction: SelectionAction.INCLUDE,
          },
        ),
      ],
    );
```

The tableMappings object takes care of assigning the rules a name and id if not specified and comes with a format method, see below.
Finally, we can write the replication in itself:

```python
new dms.CfnReplicationConfig(this, 'ReplicationConfig', {
  computeConfig: computeConfig,
  replicationConfigIdentifier: 'replicationConfigIdentifier',
  replicationType: ReplicationTypes.FULL_LOAD,
  sourceEndpointArn: this.source.ref,
  tableMappings: tableMappings.format(),
  targetEndpointArn: this.target.ref,
});
```

In the example above the 'experiment' table of the database specified above will be migrated to S3, and after executing the migration, a file 'LOAD00000001' is created in the specified 'folder' in the S3 bucket.

So far I demonstrated a couple of L2 constructs for the endpoints; but an L3 construct is also available that in turn takes care of creating all the endpoints and the migration itself:

```python
const mySql2S3 = new MySql2S3(this, 'mysql2S3', {
  databaseName: ******,
  mySqlEndpointSettings: {
    secretsManagerSecretId: 'arn:aws:secretsmanager:*******',
  },
  bucketArn: bucketArn,
  tableMappings: tableMappings,
  computeConfig: computeConfig,
  replicationConfigIdentifier: '*****',
});
```

which makes migrations easier. A similar pattern exists for postgres, and more could be added in future versions.

# Contributors

Matteo Giani
Bruno Baido
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_dms as _aws_cdk_aws_dms_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="dms-patterns.BeforeImageDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "column_filter": "columnFilter",
        "column_prefix": "columnPrefix",
        "column_suffix": "columnSuffix",
    },
)
class BeforeImageDefinition:
    def __init__(
        self,
        *,
        column_filter: builtins.str,
        column_prefix: typing.Optional[builtins.str] = None,
        column_suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column_filter: 
        :param column_prefix: 
        :param column_suffix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667f9af382cf67ab293493b3b38f65d34278a9e7e71ad6c5fba49f97db7ef0b6)
            check_type(argname="argument column_filter", value=column_filter, expected_type=type_hints["column_filter"])
            check_type(argname="argument column_prefix", value=column_prefix, expected_type=type_hints["column_prefix"])
            check_type(argname="argument column_suffix", value=column_suffix, expected_type=type_hints["column_suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_filter": column_filter,
        }
        if column_prefix is not None:
            self._values["column_prefix"] = column_prefix
        if column_suffix is not None:
            self._values["column_suffix"] = column_suffix

    @builtins.property
    def column_filter(self) -> builtins.str:
        result = self._values.get("column_filter")
        assert result is not None, "Required property 'column_filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def column_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("column_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def column_suffix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("column_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeforeImageDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="dms-patterns.CapacityUnits")
class CapacityUnits(enum.Enum):
    _1 = "_1"
    _2 = "_2"
    _4 = "_4"
    _8 = "_8"
    _16 = "_16"
    _32 = "_32"
    _64 = "_64"
    _128 = "_128"
    _192 = "_192"
    _256 = "_256"
    _384 = "_384"


@jsii.data_type(
    jsii_type="dms-patterns.DataTypeParams",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "length": "length",
        "precision": "precision",
        "scale": "scale",
    },
)
class DataTypeParams:
    def __init__(
        self,
        *,
        type: builtins.str,
        length: typing.Optional[jsii.Number] = None,
        precision: typing.Optional[jsii.Number] = None,
        scale: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
    ) -> None:
        '''
        :param type: 
        :param length: 
        :param precision: 
        :param scale: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6f116624ae75de090d0dab02f53e269fe7c4be4f68398384c2bfa3c52f6d76)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument length", value=length, expected_type=type_hints["length"])
            check_type(argname="argument precision", value=precision, expected_type=type_hints["precision"])
            check_type(argname="argument scale", value=scale, expected_type=type_hints["scale"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if length is not None:
            self._values["length"] = length
        if precision is not None:
            self._values["precision"] = precision
        if scale is not None:
            self._values["scale"] = scale

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def length(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def precision(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("precision")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scale(self) -> typing.Optional[typing.Union[builtins.str, jsii.Number]]:
        result = self._values.get("scale")
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTypeParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsVpcRoleStack(
    _aws_cdk_ceddda9d.Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.DmsVpcRoleStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        stack_name: typing.Optional[builtins.str] = None,
        suppress_template_indentation: typing.Optional[builtins.bool] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param suppress_template_indentation: Enable this flag to suppress indentation in generated CloudFormation templates. If not specified, the value of the ``@aws-cdk/core:suppressTemplateIndentation`` context key will be used. If that is not specified, then the default value ``false`` will be used. Default: - the value of ``@aws-cdk/core:suppressTemplateIndentation``, or ``false`` if that is not set.
        :param synthesizer: Synthesis method to use while deploying this stack. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. If not specified, the ``defaultStackSynthesizer`` from ``App`` will be used. If that is not specified, ``DefaultStackSynthesizer`` is used if ``@aws-cdk/core:newStyleStackSynthesis`` is set to ``true`` or the CDK major version is v2. In CDK v1 ``LegacyStackSynthesizer`` is the default if no other synthesizer is specified. Default: - The synthesizer specified on ``App``, or ``DefaultStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843b532d6facd990ffa3b6ad249a450c491be54c02decf0dc747700aca51be67)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.StackProps(
            analytics_reporting=analytics_reporting,
            cross_region_references=cross_region_references,
            description=description,
            env=env,
            permissions_boundary=permissions_boundary,
            stack_name=stack_name,
            suppress_template_indentation=suppress_template_indentation,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="dmsCloudwatchRole")
    def dms_cloudwatch_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "dmsCloudwatchRole"))

    @dms_cloudwatch_role.setter
    def dms_cloudwatch_role(self, value: _aws_cdk_aws_iam_ceddda9d.Role) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7995548b12ccb95d7a5ad71d3d8059e9076888b80bb0e5e7d3490bcc273dcfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dmsCloudwatchRole", value)

    @builtins.property
    @jsii.member(jsii_name="dmsVpcRole")
    def dms_vpc_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "dmsVpcRole"))

    @dms_vpc_role.setter
    def dms_vpc_role(self, value: _aws_cdk_aws_iam_ceddda9d.Role) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e355e58daa23240631040b055b0690209970951f9f0a085aecc9d71008e46b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dmsVpcRole", value)


@jsii.enum(jsii_type="dms-patterns.EndpointEngine")
class EndpointEngine(enum.Enum):
    MYSQL = "MYSQL"
    POSTGRES = "POSTGRES"
    S3 = "S3"


@jsii.enum(jsii_type="dms-patterns.EndpointType")
class EndpointType(enum.Enum):
    SOURCE = "SOURCE"
    TARGET = "TARGET"


@jsii.data_type(
    jsii_type="dms-patterns.LobSettings",
    jsii_struct_bases=[],
    name_mapping={"bulk_max_size": "bulkMaxSize", "mode": "mode"},
)
class LobSettings:
    def __init__(
        self,
        *,
        bulk_max_size: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bulk_max_size: 
        :param mode: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f362a317b2a4c48d9f96f4e8ddfa202006971bfa58d85a7bc2ea35027b7da971)
            check_type(argname="argument bulk_max_size", value=bulk_max_size, expected_type=type_hints["bulk_max_size"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bulk_max_size is not None:
            self._values["bulk_max_size"] = bulk_max_size
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def bulk_max_size(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("bulk_max_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LobSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MySql2S3(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.MySql2S3",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_arn: builtins.str,
        database_name: builtins.str,
        my_sql_endpoint_settings: typing.Union["MySqlSettings", typing.Dict[builtins.str, typing.Any]],
        replication_config_identifier: builtins.str,
        table_mappings: "TableMappings",
        compute_config: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        replication_settings: typing.Any = None,
        s3target_endpoint_settings: typing.Optional[typing.Union["S3TargetEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        task_settings: typing.Optional["TaskSettings"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_arn: 
        :param database_name: 
        :param my_sql_endpoint_settings: 
        :param replication_config_identifier: 
        :param table_mappings: 
        :param compute_config: 
        :param replication_settings: 
        :param s3target_endpoint_settings: 
        :param task_settings: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8421fc107c5b30d6b1bba405e4c64f86fca88bfcf1b114f95182c5828f3af5c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MySql2S3Props(
            bucket_arn=bucket_arn,
            database_name=database_name,
            my_sql_endpoint_settings=my_sql_endpoint_settings,
            replication_config_identifier=replication_config_identifier,
            table_mappings=table_mappings,
            compute_config=compute_config,
            replication_settings=replication_settings,
            s3target_endpoint_settings=s3target_endpoint_settings,
            task_settings=task_settings,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "MySqlEndpoint":
        return typing.cast("MySqlEndpoint", jsii.get(self, "source"))

    @source.setter
    def source(self, value: "MySqlEndpoint") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c02ae8d7d9825f132aa35849afcd7bcf5d204374923a3ecf283b00354e93d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "S3TargetEndpoint":
        return typing.cast("S3TargetEndpoint", jsii.get(self, "target"))

    @target.setter
    def target(self, value: "S3TargetEndpoint") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c006d4a0822f1edc4d418bbbbb0fe55cec899bbb79b77fe3be3d564414a9a765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)


@jsii.data_type(
    jsii_type="dms-patterns.MySql2S3Props",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "database_name": "databaseName",
        "my_sql_endpoint_settings": "mySqlEndpointSettings",
        "replication_config_identifier": "replicationConfigIdentifier",
        "table_mappings": "tableMappings",
        "compute_config": "computeConfig",
        "replication_settings": "replicationSettings",
        "s3target_endpoint_settings": "s3targetEndpointSettings",
        "task_settings": "taskSettings",
    },
)
class MySql2S3Props:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        database_name: builtins.str,
        my_sql_endpoint_settings: typing.Union["MySqlSettings", typing.Dict[builtins.str, typing.Any]],
        replication_config_identifier: builtins.str,
        table_mappings: "TableMappings",
        compute_config: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        replication_settings: typing.Any = None,
        s3target_endpoint_settings: typing.Optional[typing.Union["S3TargetEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        task_settings: typing.Optional["TaskSettings"] = None,
    ) -> None:
        '''
        :param bucket_arn: 
        :param database_name: 
        :param my_sql_endpoint_settings: 
        :param replication_config_identifier: 
        :param table_mappings: 
        :param compute_config: 
        :param replication_settings: 
        :param s3target_endpoint_settings: 
        :param task_settings: 
        '''
        if isinstance(my_sql_endpoint_settings, dict):
            my_sql_endpoint_settings = MySqlSettings(**my_sql_endpoint_settings)
        if isinstance(compute_config, dict):
            compute_config = _aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty(**compute_config)
        if isinstance(s3target_endpoint_settings, dict):
            s3target_endpoint_settings = S3TargetEndpointSettings(**s3target_endpoint_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a38656d8900cd716870b31d5f1dad68ff4a4f4204729f0b7335fa160d5fe00e)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument my_sql_endpoint_settings", value=my_sql_endpoint_settings, expected_type=type_hints["my_sql_endpoint_settings"])
            check_type(argname="argument replication_config_identifier", value=replication_config_identifier, expected_type=type_hints["replication_config_identifier"])
            check_type(argname="argument table_mappings", value=table_mappings, expected_type=type_hints["table_mappings"])
            check_type(argname="argument compute_config", value=compute_config, expected_type=type_hints["compute_config"])
            check_type(argname="argument replication_settings", value=replication_settings, expected_type=type_hints["replication_settings"])
            check_type(argname="argument s3target_endpoint_settings", value=s3target_endpoint_settings, expected_type=type_hints["s3target_endpoint_settings"])
            check_type(argname="argument task_settings", value=task_settings, expected_type=type_hints["task_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "database_name": database_name,
            "my_sql_endpoint_settings": my_sql_endpoint_settings,
            "replication_config_identifier": replication_config_identifier,
            "table_mappings": table_mappings,
        }
        if compute_config is not None:
            self._values["compute_config"] = compute_config
        if replication_settings is not None:
            self._values["replication_settings"] = replication_settings
        if s3target_endpoint_settings is not None:
            self._values["s3target_endpoint_settings"] = s3target_endpoint_settings
        if task_settings is not None:
            self._values["task_settings"] = task_settings

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_name(self) -> builtins.str:
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def my_sql_endpoint_settings(self) -> "MySqlSettings":
        result = self._values.get("my_sql_endpoint_settings")
        assert result is not None, "Required property 'my_sql_endpoint_settings' is missing"
        return typing.cast("MySqlSettings", result)

    @builtins.property
    def replication_config_identifier(self) -> builtins.str:
        result = self._values.get("replication_config_identifier")
        assert result is not None, "Required property 'replication_config_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_mappings(self) -> "TableMappings":
        result = self._values.get("table_mappings")
        assert result is not None, "Required property 'table_mappings' is missing"
        return typing.cast("TableMappings", result)

    @builtins.property
    def compute_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty]:
        result = self._values.get("compute_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty], result)

    @builtins.property
    def replication_settings(self) -> typing.Any:
        result = self._values.get("replication_settings")
        return typing.cast(typing.Any, result)

    @builtins.property
    def s3target_endpoint_settings(self) -> typing.Optional["S3TargetEndpointSettings"]:
        result = self._values.get("s3target_endpoint_settings")
        return typing.cast(typing.Optional["S3TargetEndpointSettings"], result)

    @builtins.property
    def task_settings(self) -> typing.Optional["TaskSettings"]:
        result = self._values.get("task_settings")
        return typing.cast(typing.Optional["TaskSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MySql2S3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MySqlEndpoint(
    _aws_cdk_aws_dms_ceddda9d.CfnEndpoint,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.MySqlEndpoint",
):
    '''An endpoint for a MySQL source.

    This construct creates a role for DMS to access the secrets manager secret.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        database_name: builtins.str,
        endpoint_identifier: builtins.str,
        endpoint_type: builtins.str,
        my_sql_endpoint_settings: typing.Union["MySqlSettings", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param database_name: The database name on the MongoDB source endpoint.
        :param endpoint_identifier: The database endpoint identifier. Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.
        :param endpoint_type: The type of endpoint.
        :param my_sql_endpoint_settings: The settings for the mysql endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5bc95e368ec4b22334846ac3f52325fe466b8b61f0343e121ca0b76b643ecb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MySqlProps(
            database_name=database_name,
            endpoint_identifier=endpoint_identifier,
            endpoint_type=endpoint_type,
            my_sql_endpoint_settings=my_sql_endpoint_settings,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="dms-patterns.MySqlProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "endpoint_identifier": "endpointIdentifier",
        "endpoint_type": "endpointType",
        "my_sql_endpoint_settings": "mySqlEndpointSettings",
    },
)
class MySqlProps:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        endpoint_identifier: builtins.str,
        endpoint_type: builtins.str,
        my_sql_endpoint_settings: typing.Union["MySqlSettings", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param database_name: The database name on the MongoDB source endpoint.
        :param endpoint_identifier: The database endpoint identifier. Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.
        :param endpoint_type: The type of endpoint.
        :param my_sql_endpoint_settings: The settings for the mysql endpoint.
        '''
        if isinstance(my_sql_endpoint_settings, dict):
            my_sql_endpoint_settings = MySqlSettings(**my_sql_endpoint_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ec09267c8ea6591e86ffd1305748c424caece1f84f49a7d8997080bf89ac75)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument endpoint_identifier", value=endpoint_identifier, expected_type=type_hints["endpoint_identifier"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument my_sql_endpoint_settings", value=my_sql_endpoint_settings, expected_type=type_hints["my_sql_endpoint_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "endpoint_identifier": endpoint_identifier,
            "endpoint_type": endpoint_type,
            "my_sql_endpoint_settings": my_sql_endpoint_settings,
        }

    @builtins.property
    def database_name(self) -> builtins.str:
        '''The database name on the MongoDB source endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-databasename
        '''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_identifier(self) -> builtins.str:
        '''The database endpoint identifier.

        Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-endpointidentifier
        '''
        result = self._values.get("endpoint_identifier")
        assert result is not None, "Required property 'endpoint_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_type(self) -> builtins.str:
        '''The type of endpoint.'''
        result = self._values.get("endpoint_type")
        assert result is not None, "Required property 'endpoint_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def my_sql_endpoint_settings(self) -> "MySqlSettings":
        '''The settings for the mysql endpoint.'''
        result = self._values.get("my_sql_endpoint_settings")
        assert result is not None, "Required property 'my_sql_endpoint_settings' is missing"
        return typing.cast("MySqlSettings", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MySqlProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="dms-patterns.MySqlSettings",
    jsii_struct_bases=[],
    name_mapping={
        "secrets_manager_secret_id": "secretsManagerSecretId",
        "after_connect_script": "afterConnectScript",
        "clean_source_metadata_on_mismatch": "cleanSourceMetadataOnMismatch",
        "events_poll_interval": "eventsPollInterval",
        "server_timezone": "serverTimezone",
        "ssl_mode": "sslMode",
    },
)
class MySqlSettings:
    def __init__(
        self,
        *,
        secrets_manager_secret_id: builtins.str,
        after_connect_script: typing.Optional[builtins.str] = None,
        clean_source_metadata_on_mismatch: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        events_poll_interval: typing.Optional[jsii.Number] = None,
        server_timezone: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the MySQL endpoint connection details.
        :param after_connect_script: Code to run after connecting. This parameter should contain the code itself, not the name of a file containing the code.
        :param clean_source_metadata_on_mismatch: Cleans and recreates table metadata information on the replication instance when a mismatch occurs. For example, in a situation where running an alter DDL on the table could result in different information about the table cached in the replication instance.
        :param events_poll_interval: Specifies how often to check the binary log for new changes/events when the database is idle. The default is five seconds. Example: ``eventsPollInterval=5;`` In the example, AWS DMS checks for changes in the binary logs every five seconds.
        :param server_timezone: Specifies the time zone for the source MySQL database. Don't enclose time zones in single quotation marks. Example: ``serverTimezone=US/Pacific;``
        :param ssl_mode: The Secure Sockets Layer (SSL) mode to use for the SSL connection. The default is ``none`` . .. epigraph:: When ``engine_name`` is set to S3, the only allowed value is ``none`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be5b4fcc2c06c6dddd07db0353bf6c0ab65f4be51ff6ff209848fd89f5f14b83)
            check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
            check_type(argname="argument after_connect_script", value=after_connect_script, expected_type=type_hints["after_connect_script"])
            check_type(argname="argument clean_source_metadata_on_mismatch", value=clean_source_metadata_on_mismatch, expected_type=type_hints["clean_source_metadata_on_mismatch"])
            check_type(argname="argument events_poll_interval", value=events_poll_interval, expected_type=type_hints["events_poll_interval"])
            check_type(argname="argument server_timezone", value=server_timezone, expected_type=type_hints["server_timezone"])
            check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secrets_manager_secret_id": secrets_manager_secret_id,
        }
        if after_connect_script is not None:
            self._values["after_connect_script"] = after_connect_script
        if clean_source_metadata_on_mismatch is not None:
            self._values["clean_source_metadata_on_mismatch"] = clean_source_metadata_on_mismatch
        if events_poll_interval is not None:
            self._values["events_poll_interval"] = events_poll_interval
        if server_timezone is not None:
            self._values["server_timezone"] = server_timezone
        if ssl_mode is not None:
            self._values["ssl_mode"] = ssl_mode

    @builtins.property
    def secrets_manager_secret_id(self) -> builtins.str:
        '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the MySQL endpoint connection details.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-secretsmanagersecretid
        '''
        result = self._values.get("secrets_manager_secret_id")
        assert result is not None, "Required property 'secrets_manager_secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def after_connect_script(self) -> typing.Optional[builtins.str]:
        '''Code to run after connecting.

        This parameter should contain the code itself, not the name of a file containing the code.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-afterconnectscript
        '''
        result = self._values.get("after_connect_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clean_source_metadata_on_mismatch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Cleans and recreates table metadata information on the replication instance when a mismatch occurs.

        For example, in a situation where running an alter DDL on the table could result in different information about the table cached in the replication instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-cleansourcemetadataonmismatch
        '''
        result = self._values.get("clean_source_metadata_on_mismatch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def events_poll_interval(self) -> typing.Optional[jsii.Number]:
        '''Specifies how often to check the binary log for new changes/events when the database is idle.

        The default is five seconds.

        Example: ``eventsPollInterval=5;``

        In the example, AWS DMS checks for changes in the binary logs every five seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mysqlsettings.html#cfn-dms-endpoint-mysqlsettings-eventspollinterval
        '''
        result = self._values.get("events_poll_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def server_timezone(self) -> typing.Optional[builtins.str]:
        '''Specifies the time zone for the source MySQL database. Don't enclose time zones in single quotation marks.

        Example: ``serverTimezone=US/Pacific;``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-gcpmysqlsettings.html#cfn-dms-endpoint-gcpmysqlsettings-servertimezone
        '''
        result = self._values.get("server_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        '''The Secure Sockets Layer (SSL) mode to use for the SSL connection. The default is ``none`` .

        .. epigraph::

           When ``engine_name`` is set to S3, the only allowed value is ``none`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-sslmode
        '''
        result = self._values.get("ssl_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MySqlSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="dms-patterns.ObjectLocator",
    jsii_struct_bases=[],
    name_mapping={"schema_name": "schemaName", "table_name": "tableName"},
)
class ObjectLocator:
    def __init__(
        self,
        *,
        schema_name: builtins.str,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_name: 
        :param table_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdca11b6edf0314b444ecefb2470310061565728c95917175376d6f74f579909)
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema_name": schema_name,
        }
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def schema_name(self) -> builtins.str:
        result = self._values.get("schema_name")
        assert result is not None, "Required property 'schema_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObjectLocator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="dms-patterns.ParallelLoad",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "batch_size": "batchSize",
        "boundaries": "boundaries",
        "collection_count_from_metadata": "collectionCountFromMetadata",
        "columns": "columns",
        "max_records_skip_per_page": "maxRecordsSkipPerPage",
        "number_of_partitions": "numberOfPartitions",
        "partitions": "partitions",
        "subpartitions": "subpartitions",
    },
)
class ParallelLoad:
    def __init__(
        self,
        *,
        type: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        boundaries: typing.Optional[typing.Sequence[typing.Sequence[typing.Any]]] = None,
        collection_count_from_metadata: typing.Optional[builtins.bool] = None,
        columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_records_skip_per_page: typing.Optional[jsii.Number] = None,
        number_of_partitions: typing.Optional[jsii.Number] = None,
        partitions: typing.Optional[typing.Sequence[builtins.str]] = None,
        subpartitions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: 
        :param batch_size: 
        :param boundaries: 
        :param collection_count_from_metadata: 
        :param columns: 
        :param max_records_skip_per_page: 
        :param number_of_partitions: 
        :param partitions: 
        :param subpartitions: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b04864cd73a655bdf0e25b5109c21dc8d7fb684d34856b872bd9f499292d13)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument boundaries", value=boundaries, expected_type=type_hints["boundaries"])
            check_type(argname="argument collection_count_from_metadata", value=collection_count_from_metadata, expected_type=type_hints["collection_count_from_metadata"])
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument max_records_skip_per_page", value=max_records_skip_per_page, expected_type=type_hints["max_records_skip_per_page"])
            check_type(argname="argument number_of_partitions", value=number_of_partitions, expected_type=type_hints["number_of_partitions"])
            check_type(argname="argument partitions", value=partitions, expected_type=type_hints["partitions"])
            check_type(argname="argument subpartitions", value=subpartitions, expected_type=type_hints["subpartitions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if boundaries is not None:
            self._values["boundaries"] = boundaries
        if collection_count_from_metadata is not None:
            self._values["collection_count_from_metadata"] = collection_count_from_metadata
        if columns is not None:
            self._values["columns"] = columns
        if max_records_skip_per_page is not None:
            self._values["max_records_skip_per_page"] = max_records_skip_per_page
        if number_of_partitions is not None:
            self._values["number_of_partitions"] = number_of_partitions
        if partitions is not None:
            self._values["partitions"] = partitions
        if subpartitions is not None:
            self._values["subpartitions"] = subpartitions

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boundaries(self) -> typing.Optional[typing.List[typing.List[typing.Any]]]:
        result = self._values.get("boundaries")
        return typing.cast(typing.Optional[typing.List[typing.List[typing.Any]]], result)

    @builtins.property
    def collection_count_from_metadata(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("collection_count_from_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def columns(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("columns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_records_skip_per_page(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_records_skip_per_page")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def number_of_partitions(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("number_of_partitions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def partitions(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("partitions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subpartitions(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("subpartitions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParallelLoad(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PostgreSQLEndpoint(
    _aws_cdk_aws_dms_ceddda9d.CfnEndpoint,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.PostgreSQLEndpoint",
):
    '''An endpoint for a Postgres source.

    This construct creates a role for DMS to access the secrets manager secret.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        database_name: builtins.str,
        endpoint_identifier: builtins.str,
        endpoint_type: builtins.str,
        postgres_endpoint_settings: typing.Union["PostgreSqlSettings", typing.Dict[builtins.str, typing.Any]],
        port: typing.Optional[jsii.Number] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param database_name: The database name on the MongoDB source endpoint.
        :param endpoint_identifier: The database endpoint identifier. Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.
        :param endpoint_type: The type of endpoint.
        :param postgres_endpoint_settings: The settings for the source postgres endpoint.
        :param port: The port value for the source endpoint.
        :param ssl_mode: The Secure Sockets Layer (SSL) mode to use for the SSL connection. The default is ``none`` . .. epigraph:: When ``engine_name`` is set to S3, the only allowed value is ``none`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92befc2f4d59e8aa32ef5975d2f8b4d31cb75cf228b27e2b58db90819db62d16)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PostgresProps(
            database_name=database_name,
            endpoint_identifier=endpoint_identifier,
            endpoint_type=endpoint_type,
            postgres_endpoint_settings=postgres_endpoint_settings,
            port=port,
            ssl_mode=ssl_mode,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="dms-patterns.PostgreSqlSettings",
    jsii_struct_bases=[],
    name_mapping={
        "secrets_manager_secret_id": "secretsManagerSecretId",
        "capture_ddls": "captureDdls",
        "ddl_artifacts_schema": "ddlArtifactsSchema",
        "execute_timeout": "executeTimeout",
        "fail_tasks_on_lob_truncation": "failTasksOnLobTruncation",
        "heartbeat_frequency": "heartbeatFrequency",
        "heartbeat_schema": "heartbeatSchema",
        "map_boolean_as_boolean": "mapBooleanAsBoolean",
        "plugin_name": "pluginName",
        "slot_name": "slotName",
    },
)
class PostgreSqlSettings:
    def __init__(
        self,
        *,
        secrets_manager_secret_id: builtins.str,
        capture_ddls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ddl_artifacts_schema: typing.Optional[builtins.str] = None,
        execute_timeout: typing.Optional[jsii.Number] = None,
        fail_tasks_on_lob_truncation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        heartbeat_frequency: typing.Optional[jsii.Number] = None,
        heartbeat_schema: typing.Optional[builtins.str] = None,
        map_boolean_as_boolean: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        slot_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secrets_manager_secret_id: The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the Amazon Redshift endpoint connection details.
        :param capture_ddls: To capture DDL events, AWS DMS creates various artifacts in the PostgreSQL database when the task starts. You can later remove these artifacts. If this value is set to ``N`` , you don't have to create tables or triggers on the source database.
        :param ddl_artifacts_schema: The schema in which the operational DDL database artifacts are created. Example: ``ddlArtifactsSchema=xyzddlschema;``
        :param execute_timeout: Sets the client statement timeout for the PostgreSQL instance, in seconds. The default value is 60 seconds. Example: ``executeTimeout=100;``
        :param fail_tasks_on_lob_truncation: When set to ``true`` , this value causes a task to fail if the actual size of a LOB column is greater than the specified ``LobMaxSize`` . If task is set to Limited LOB mode and this option is set to true, the task fails instead of truncating the LOB data.
        :param heartbeat_frequency: Sets the WAL heartbeat frequency (in minutes).
        :param heartbeat_schema: Sets the schema in which the heartbeat artifacts are created.
        :param map_boolean_as_boolean: When true, lets PostgreSQL migrate the boolean type as boolean. By default, PostgreSQL migrates booleans as ``varchar(5)`` . You must set this setting on both the source and target endpoints for it to take effect.
        :param plugin_name: Specifies the plugin to use to create a replication slot.
        :param slot_name: Sets the name of a previously created logical replication slot for a change data capture (CDC) load of the PostgreSQL source instance. When used with the ``CdcStartPosition`` request parameter for the AWS DMS API , this attribute also makes it possible to use native CDC start points. DMS verifies that the specified logical replication slot exists before starting the CDC load task. It also verifies that the task was created with a valid setting of ``CdcStartPosition`` . If the specified slot doesn't exist or the task doesn't have a valid ``CdcStartPosition`` setting, DMS raises an error. For more information about setting the ``CdcStartPosition`` request parameter, see `Determining a CDC native start point <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html#CHAP_Task.CDC.StartPoint.Native>`_ in the *AWS Database Migration Service User Guide* . For more information about using ``CdcStartPosition`` , see `CreateReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_CreateReplicationTask.html>`_ , `StartReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_StartReplicationTask.html>`_ , and `ModifyReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_ModifyReplicationTask.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825a166842d541be750f985e572e19c7fd47bb992e3fe9cf458d391be4d579a1)
            check_type(argname="argument secrets_manager_secret_id", value=secrets_manager_secret_id, expected_type=type_hints["secrets_manager_secret_id"])
            check_type(argname="argument capture_ddls", value=capture_ddls, expected_type=type_hints["capture_ddls"])
            check_type(argname="argument ddl_artifacts_schema", value=ddl_artifacts_schema, expected_type=type_hints["ddl_artifacts_schema"])
            check_type(argname="argument execute_timeout", value=execute_timeout, expected_type=type_hints["execute_timeout"])
            check_type(argname="argument fail_tasks_on_lob_truncation", value=fail_tasks_on_lob_truncation, expected_type=type_hints["fail_tasks_on_lob_truncation"])
            check_type(argname="argument heartbeat_frequency", value=heartbeat_frequency, expected_type=type_hints["heartbeat_frequency"])
            check_type(argname="argument heartbeat_schema", value=heartbeat_schema, expected_type=type_hints["heartbeat_schema"])
            check_type(argname="argument map_boolean_as_boolean", value=map_boolean_as_boolean, expected_type=type_hints["map_boolean_as_boolean"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument slot_name", value=slot_name, expected_type=type_hints["slot_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secrets_manager_secret_id": secrets_manager_secret_id,
        }
        if capture_ddls is not None:
            self._values["capture_ddls"] = capture_ddls
        if ddl_artifacts_schema is not None:
            self._values["ddl_artifacts_schema"] = ddl_artifacts_schema
        if execute_timeout is not None:
            self._values["execute_timeout"] = execute_timeout
        if fail_tasks_on_lob_truncation is not None:
            self._values["fail_tasks_on_lob_truncation"] = fail_tasks_on_lob_truncation
        if heartbeat_frequency is not None:
            self._values["heartbeat_frequency"] = heartbeat_frequency
        if heartbeat_schema is not None:
            self._values["heartbeat_schema"] = heartbeat_schema
        if map_boolean_as_boolean is not None:
            self._values["map_boolean_as_boolean"] = map_boolean_as_boolean
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if slot_name is not None:
            self._values["slot_name"] = slot_name

    @builtins.property
    def secrets_manager_secret_id(self) -> builtins.str:
        '''The full ARN, partial ARN, or display name of the ``SecretsManagerSecret`` that contains the Amazon Redshift endpoint connection details.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-secretsmanagersecretid
        '''
        result = self._values.get("secrets_manager_secret_id")
        assert result is not None, "Required property 'secrets_manager_secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capture_ddls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''To capture DDL events, AWS DMS creates various artifacts in the PostgreSQL database when the task starts.

        You can later remove these artifacts.

        If this value is set to ``N`` , you don't have to create tables or triggers on the source database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-captureddls
        '''
        result = self._values.get("capture_ddls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def ddl_artifacts_schema(self) -> typing.Optional[builtins.str]:
        '''The schema in which the operational DDL database artifacts are created.

        Example: ``ddlArtifactsSchema=xyzddlschema;``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-ddlartifactsschema
        '''
        result = self._values.get("ddl_artifacts_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execute_timeout(self) -> typing.Optional[jsii.Number]:
        '''Sets the client statement timeout for the PostgreSQL instance, in seconds. The default value is 60 seconds.

        Example: ``executeTimeout=100;``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-executetimeout
        '''
        result = self._values.get("execute_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fail_tasks_on_lob_truncation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When set to ``true`` , this value causes a task to fail if the actual size of a LOB column is greater than the specified ``LobMaxSize`` .

        If task is set to Limited LOB mode and this option is set to true, the task fails instead of truncating the LOB data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-failtasksonlobtruncation
        '''
        result = self._values.get("fail_tasks_on_lob_truncation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def heartbeat_frequency(self) -> typing.Optional[jsii.Number]:
        '''Sets the WAL heartbeat frequency (in minutes).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-heartbeatfrequency
        '''
        result = self._values.get("heartbeat_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def heartbeat_schema(self) -> typing.Optional[builtins.str]:
        '''Sets the schema in which the heartbeat artifacts are created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-heartbeatschema
        '''
        result = self._values.get("heartbeat_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def map_boolean_as_boolean(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When true, lets PostgreSQL migrate the boolean type as boolean.

        By default, PostgreSQL migrates booleans as ``varchar(5)`` . You must set this setting on both the source and target endpoints for it to take effect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-mapbooleanasboolean
        '''
        result = self._values.get("map_boolean_as_boolean")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the plugin to use to create a replication slot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-pluginname
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slot_name(self) -> typing.Optional[builtins.str]:
        '''Sets the name of a previously created logical replication slot for a change data capture (CDC) load of the PostgreSQL source instance.

        When used with the ``CdcStartPosition`` request parameter for the AWS DMS API , this attribute also makes it possible to use native CDC start points. DMS verifies that the specified logical replication slot exists before starting the CDC load task. It also verifies that the task was created with a valid setting of ``CdcStartPosition`` . If the specified slot doesn't exist or the task doesn't have a valid ``CdcStartPosition`` setting, DMS raises an error.

        For more information about setting the ``CdcStartPosition`` request parameter, see `Determining a CDC native start point <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html#CHAP_Task.CDC.StartPoint.Native>`_ in the *AWS Database Migration Service User Guide* . For more information about using ``CdcStartPosition`` , see `CreateReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_CreateReplicationTask.html>`_ , `StartReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_StartReplicationTask.html>`_ , and `ModifyReplicationTask <https://docs.aws.amazon.com/dms/latest/APIReference/API_ModifyReplicationTask.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-postgresqlsettings.html#cfn-dms-endpoint-postgresqlsettings-slotname
        '''
        result = self._values.get("slot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgreSqlSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Postgres2S3(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.Postgres2S3",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_arn: builtins.str,
        database_name: builtins.str,
        postgres_endpoint_settings: typing.Union[PostgreSqlSettings, typing.Dict[builtins.str, typing.Any]],
        replication_config_identifier: builtins.str,
        table_mappings: "TableMappings",
        compute_config: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        replication_settings: typing.Any = None,
        s3target_endpoint_settings: typing.Optional[typing.Union["S3TargetEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        task_settings: typing.Optional["TaskSettings"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_arn: 
        :param database_name: 
        :param postgres_endpoint_settings: 
        :param replication_config_identifier: 
        :param table_mappings: 
        :param compute_config: 
        :param replication_settings: 
        :param s3target_endpoint_settings: 
        :param task_settings: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b7eb97a04f77db1abbb83e5bef8f0f8b611eda71d81076a7dc2c49ae8f8b11)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Postgres2S3Props(
            bucket_arn=bucket_arn,
            database_name=database_name,
            postgres_endpoint_settings=postgres_endpoint_settings,
            replication_config_identifier=replication_config_identifier,
            table_mappings=table_mappings,
            compute_config=compute_config,
            replication_settings=replication_settings,
            s3target_endpoint_settings=s3target_endpoint_settings,
            task_settings=task_settings,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> PostgreSQLEndpoint:
        return typing.cast(PostgreSQLEndpoint, jsii.get(self, "source"))

    @source.setter
    def source(self, value: PostgreSQLEndpoint) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0a7364f6600a9916d4829e7729eb494622007b2a7ea54da1e5fd8429ee28aca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "S3TargetEndpoint":
        return typing.cast("S3TargetEndpoint", jsii.get(self, "target"))

    @target.setter
    def target(self, value: "S3TargetEndpoint") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a1fabb06c784c92505891c1da8270dbe1db8cb220fc612efff2947078e9c16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)


@jsii.data_type(
    jsii_type="dms-patterns.Postgres2S3Props",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "database_name": "databaseName",
        "postgres_endpoint_settings": "postgresEndpointSettings",
        "replication_config_identifier": "replicationConfigIdentifier",
        "table_mappings": "tableMappings",
        "compute_config": "computeConfig",
        "replication_settings": "replicationSettings",
        "s3target_endpoint_settings": "s3targetEndpointSettings",
        "task_settings": "taskSettings",
    },
)
class Postgres2S3Props:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        database_name: builtins.str,
        postgres_endpoint_settings: typing.Union[PostgreSqlSettings, typing.Dict[builtins.str, typing.Any]],
        replication_config_identifier: builtins.str,
        table_mappings: "TableMappings",
        compute_config: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        replication_settings: typing.Any = None,
        s3target_endpoint_settings: typing.Optional[typing.Union["S3TargetEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        task_settings: typing.Optional["TaskSettings"] = None,
    ) -> None:
        '''
        :param bucket_arn: 
        :param database_name: 
        :param postgres_endpoint_settings: 
        :param replication_config_identifier: 
        :param table_mappings: 
        :param compute_config: 
        :param replication_settings: 
        :param s3target_endpoint_settings: 
        :param task_settings: 
        '''
        if isinstance(postgres_endpoint_settings, dict):
            postgres_endpoint_settings = PostgreSqlSettings(**postgres_endpoint_settings)
        if isinstance(compute_config, dict):
            compute_config = _aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty(**compute_config)
        if isinstance(s3target_endpoint_settings, dict):
            s3target_endpoint_settings = S3TargetEndpointSettings(**s3target_endpoint_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15f1eedac7dd2787fe56212e68f33d80c6a0f8dbd41c047f80f4be82ec402aa)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument postgres_endpoint_settings", value=postgres_endpoint_settings, expected_type=type_hints["postgres_endpoint_settings"])
            check_type(argname="argument replication_config_identifier", value=replication_config_identifier, expected_type=type_hints["replication_config_identifier"])
            check_type(argname="argument table_mappings", value=table_mappings, expected_type=type_hints["table_mappings"])
            check_type(argname="argument compute_config", value=compute_config, expected_type=type_hints["compute_config"])
            check_type(argname="argument replication_settings", value=replication_settings, expected_type=type_hints["replication_settings"])
            check_type(argname="argument s3target_endpoint_settings", value=s3target_endpoint_settings, expected_type=type_hints["s3target_endpoint_settings"])
            check_type(argname="argument task_settings", value=task_settings, expected_type=type_hints["task_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "database_name": database_name,
            "postgres_endpoint_settings": postgres_endpoint_settings,
            "replication_config_identifier": replication_config_identifier,
            "table_mappings": table_mappings,
        }
        if compute_config is not None:
            self._values["compute_config"] = compute_config
        if replication_settings is not None:
            self._values["replication_settings"] = replication_settings
        if s3target_endpoint_settings is not None:
            self._values["s3target_endpoint_settings"] = s3target_endpoint_settings
        if task_settings is not None:
            self._values["task_settings"] = task_settings

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_name(self) -> builtins.str:
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgres_endpoint_settings(self) -> PostgreSqlSettings:
        result = self._values.get("postgres_endpoint_settings")
        assert result is not None, "Required property 'postgres_endpoint_settings' is missing"
        return typing.cast(PostgreSqlSettings, result)

    @builtins.property
    def replication_config_identifier(self) -> builtins.str:
        result = self._values.get("replication_config_identifier")
        assert result is not None, "Required property 'replication_config_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_mappings(self) -> "TableMappings":
        result = self._values.get("table_mappings")
        assert result is not None, "Required property 'table_mappings' is missing"
        return typing.cast("TableMappings", result)

    @builtins.property
    def compute_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty]:
        result = self._values.get("compute_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty], result)

    @builtins.property
    def replication_settings(self) -> typing.Any:
        result = self._values.get("replication_settings")
        return typing.cast(typing.Any, result)

    @builtins.property
    def s3target_endpoint_settings(self) -> typing.Optional["S3TargetEndpointSettings"]:
        result = self._values.get("s3target_endpoint_settings")
        return typing.cast(typing.Optional["S3TargetEndpointSettings"], result)

    @builtins.property
    def task_settings(self) -> typing.Optional["TaskSettings"]:
        result = self._values.get("task_settings")
        return typing.cast(typing.Optional["TaskSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Postgres2S3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="dms-patterns.PostgresProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "endpoint_identifier": "endpointIdentifier",
        "endpoint_type": "endpointType",
        "postgres_endpoint_settings": "postgresEndpointSettings",
        "port": "port",
        "ssl_mode": "sslMode",
    },
)
class PostgresProps:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        endpoint_identifier: builtins.str,
        endpoint_type: builtins.str,
        postgres_endpoint_settings: typing.Union[PostgreSqlSettings, typing.Dict[builtins.str, typing.Any]],
        port: typing.Optional[jsii.Number] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: The database name on the MongoDB source endpoint.
        :param endpoint_identifier: The database endpoint identifier. Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.
        :param endpoint_type: The type of endpoint.
        :param postgres_endpoint_settings: The settings for the source postgres endpoint.
        :param port: The port value for the source endpoint.
        :param ssl_mode: The Secure Sockets Layer (SSL) mode to use for the SSL connection. The default is ``none`` . .. epigraph:: When ``engine_name`` is set to S3, the only allowed value is ``none`` .
        '''
        if isinstance(postgres_endpoint_settings, dict):
            postgres_endpoint_settings = PostgreSqlSettings(**postgres_endpoint_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cddd0113a73e09bfde59d3dda86fce808a8794864fd048933a6718c3909dcf22)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument endpoint_identifier", value=endpoint_identifier, expected_type=type_hints["endpoint_identifier"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument postgres_endpoint_settings", value=postgres_endpoint_settings, expected_type=type_hints["postgres_endpoint_settings"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "endpoint_identifier": endpoint_identifier,
            "endpoint_type": endpoint_type,
            "postgres_endpoint_settings": postgres_endpoint_settings,
        }
        if port is not None:
            self._values["port"] = port
        if ssl_mode is not None:
            self._values["ssl_mode"] = ssl_mode

    @builtins.property
    def database_name(self) -> builtins.str:
        '''The database name on the MongoDB source endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-databasename
        '''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_identifier(self) -> builtins.str:
        '''The database endpoint identifier.

        Identifiers must begin with a letter and must contain only ASCII letters, digits, and hyphens. They can't end with a hyphen, or contain two consecutive hyphens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-endpointidentifier
        '''
        result = self._values.get("endpoint_identifier")
        assert result is not None, "Required property 'endpoint_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_type(self) -> builtins.str:
        '''The type of endpoint.'''
        result = self._values.get("endpoint_type")
        assert result is not None, "Required property 'endpoint_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgres_endpoint_settings(self) -> PostgreSqlSettings:
        '''The settings for the source postgres endpoint.'''
        result = self._values.get("postgres_endpoint_settings")
        assert result is not None, "Required property 'postgres_endpoint_settings' is missing"
        return typing.cast(PostgreSqlSettings, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port value for the source endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        '''The Secure Sockets Layer (SSL) mode to use for the SSL connection. The default is ``none`` .

        .. epigraph::

           When ``engine_name`` is set to S3, the only allowed value is ``none`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-sslmode
        '''
        result = self._values.get("ssl_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgresProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="dms-patterns.PrimaryKeyDefinition",
    jsii_struct_bases=[],
    name_mapping={"columns": "columns", "name": "name", "origin": "origin"},
)
class PrimaryKeyDefinition:
    def __init__(
        self,
        *,
        columns: typing.Sequence[builtins.str],
        name: builtins.str,
        origin: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param columns: 
        :param name: 
        :param origin: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1911bb297fa0811b0ce4984bb2a990c557520cc0ff87f3b86640baa9b78f01d)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
            "name": name,
        }
        if origin is not None:
            self._values["origin"] = origin

    @builtins.property
    def columns(self) -> typing.List[builtins.str]:
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrimaryKeyDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="dms-patterns.ReplicationTypes")
class ReplicationTypes(enum.Enum):
    FULL_LOAD = "FULL_LOAD"
    CDC = "CDC"
    FULL_LOAD_AND_CDC = "FULL_LOAD_AND_CDC"


class Rule(metaclass=jsii.JSIIMeta, jsii_type="dms-patterns.Rule"):
    def __init__(
        self,
        *,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        load_order: typing.Optional[jsii.Number] = None,
        rule_action: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filters: 
        :param load_order: 
        :param rule_action: 
        :param rule_id: 
        :param rule_name: 
        '''
        props = RuleProps(
            filters=filters,
            load_order=load_order,
            rule_action=rule_action,
            rule_id=rule_id,
            rule_name=rule_name,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="format")
    def format(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "format", []))

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        return typing.cast(typing.Optional[typing.List[typing.Any]], jsii.get(self, "filters"))

    @filters.setter
    def filters(self, value: typing.Optional[typing.List[typing.Any]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207c6b48859ea1f50c9bbf11f2566d2b9923b91096f964cd2079d68a964b8f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filters", value)

    @builtins.property
    @jsii.member(jsii_name="loadOrder")
    def load_order(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "loadOrder"))

    @load_order.setter
    def load_order(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20724d4988391d538c8aa6181ac4d06a714127dd37dea8649aecaec36b4b6f12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadOrder", value)

    @builtins.property
    @jsii.member(jsii_name="ruleAction")
    def rule_action(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleAction"))

    @rule_action.setter
    def rule_action(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9598e29308a5c2081484b2d38a2094166354a77d50704c28c79ea8469266e22b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleAction", value)

    @builtins.property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleId"))

    @rule_id.setter
    def rule_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491f151bc24f8115e16e3ead727c88d5a24646dc4d12d70943bb9be46650030c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleId", value)

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a420fb93fe547b3b5967fee97e927e6d6bf41d1130ce8d5d7958398248f5b239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value)


@jsii.data_type(
    jsii_type="dms-patterns.RuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "filters": "filters",
        "load_order": "loadOrder",
        "rule_action": "ruleAction",
        "rule_id": "ruleId",
        "rule_name": "ruleName",
    },
)
class RuleProps:
    def __init__(
        self,
        *,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        load_order: typing.Optional[jsii.Number] = None,
        rule_action: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filters: 
        :param load_order: 
        :param rule_action: 
        :param rule_id: 
        :param rule_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a07a66781a531a483c4386a36184797fdee7e20defd89bc8ea157ece01b747)
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument load_order", value=load_order, expected_type=type_hints["load_order"])
            check_type(argname="argument rule_action", value=rule_action, expected_type=type_hints["rule_action"])
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filters is not None:
            self._values["filters"] = filters
        if load_order is not None:
            self._values["load_order"] = load_order
        if rule_action is not None:
            self._values["rule_action"] = rule_action
        if rule_id is not None:
            self._values["rule_id"] = rule_id
        if rule_name is not None:
            self._values["rule_name"] = rule_name

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def load_order(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("load_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rule_action(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="dms-patterns.RuleType")
class RuleType(enum.Enum):
    TABLE_SETTINGS = "TABLE_SETTINGS"


class S32s3(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.S32s3",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        source_bucket_arn: builtins.str,
        table_mappings: "TableMappings",
        target_bucket_arn: builtins.str,
        source_endpoint_settings: typing.Optional[typing.Union["S3SourceEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        target_endpoint_settings: typing.Optional[typing.Union["S3TargetEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        task_settings: typing.Optional["TaskSettings"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param source_bucket_arn: The arn of the S3 bucket to be used as source.
        :param table_mappings: The table mappings to be used for the replication.
        :param target_bucket_arn: The arn of the S3 bucket to be used as target.
        :param source_endpoint_settings: The settings for the source s3 endpoint.
        :param target_endpoint_settings: The settings for the source s3 endpoint.
        :param task_settings: Optional JSON settings for AWS DMS Serverless replications.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec25ea4b2542a04f088a34d74d7319dcd90a8a2065924b9ab647e3424bf5fc5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S32s3Props(
            source_bucket_arn=source_bucket_arn,
            table_mappings=table_mappings,
            target_bucket_arn=target_bucket_arn,
            source_endpoint_settings=source_endpoint_settings,
            target_endpoint_settings=target_endpoint_settings,
            task_settings=task_settings,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="replicationInstance")
    def replication_instance(self) -> _aws_cdk_aws_dms_ceddda9d.CfnReplicationInstance:
        return typing.cast(_aws_cdk_aws_dms_ceddda9d.CfnReplicationInstance, jsii.get(self, "replicationInstance"))

    @builtins.property
    @jsii.member(jsii_name="replicationTask")
    def replication_task(self) -> _aws_cdk_aws_dms_ceddda9d.CfnReplicationTask:
        return typing.cast(_aws_cdk_aws_dms_ceddda9d.CfnReplicationTask, jsii.get(self, "replicationTask"))

    @replication_task.setter
    def replication_task(
        self,
        value: _aws_cdk_aws_dms_ceddda9d.CfnReplicationTask,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c2abb42f459f87f75dbca212cf2761cefa8ab9d1913893f3d46555875c3f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationTask", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "S3SourceEndpoint":
        return typing.cast("S3SourceEndpoint", jsii.get(self, "source"))

    @source.setter
    def source(self, value: "S3SourceEndpoint") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d810c3375d81a6d1d1e310f6ee59588499bd26ce5a9857f7a4c53cc3c278a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "S3TargetEndpoint":
        return typing.cast("S3TargetEndpoint", jsii.get(self, "target"))

    @target.setter
    def target(self, value: "S3TargetEndpoint") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa4d6f2a789fbb7cb1543e06bf9c9316b1ad59934465a201ff520c50cf0bece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)


@jsii.data_type(
    jsii_type="dms-patterns.S32s3Props",
    jsii_struct_bases=[],
    name_mapping={
        "source_bucket_arn": "sourceBucketArn",
        "table_mappings": "tableMappings",
        "target_bucket_arn": "targetBucketArn",
        "source_endpoint_settings": "sourceEndpointSettings",
        "target_endpoint_settings": "targetEndpointSettings",
        "task_settings": "taskSettings",
    },
)
class S32s3Props:
    def __init__(
        self,
        *,
        source_bucket_arn: builtins.str,
        table_mappings: "TableMappings",
        target_bucket_arn: builtins.str,
        source_endpoint_settings: typing.Optional[typing.Union["S3SourceEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        target_endpoint_settings: typing.Optional[typing.Union["S3TargetEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        task_settings: typing.Optional["TaskSettings"] = None,
    ) -> None:
        '''
        :param source_bucket_arn: The arn of the S3 bucket to be used as source.
        :param table_mappings: The table mappings to be used for the replication.
        :param target_bucket_arn: The arn of the S3 bucket to be used as target.
        :param source_endpoint_settings: The settings for the source s3 endpoint.
        :param target_endpoint_settings: The settings for the source s3 endpoint.
        :param task_settings: Optional JSON settings for AWS DMS Serverless replications.
        '''
        if isinstance(source_endpoint_settings, dict):
            source_endpoint_settings = S3SourceEndpointSettings(**source_endpoint_settings)
        if isinstance(target_endpoint_settings, dict):
            target_endpoint_settings = S3TargetEndpointSettings(**target_endpoint_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6c83763074671fe62265290ad2260669fa2bc0bd70453d0a4fa2c6049f083c6)
            check_type(argname="argument source_bucket_arn", value=source_bucket_arn, expected_type=type_hints["source_bucket_arn"])
            check_type(argname="argument table_mappings", value=table_mappings, expected_type=type_hints["table_mappings"])
            check_type(argname="argument target_bucket_arn", value=target_bucket_arn, expected_type=type_hints["target_bucket_arn"])
            check_type(argname="argument source_endpoint_settings", value=source_endpoint_settings, expected_type=type_hints["source_endpoint_settings"])
            check_type(argname="argument target_endpoint_settings", value=target_endpoint_settings, expected_type=type_hints["target_endpoint_settings"])
            check_type(argname="argument task_settings", value=task_settings, expected_type=type_hints["task_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_bucket_arn": source_bucket_arn,
            "table_mappings": table_mappings,
            "target_bucket_arn": target_bucket_arn,
        }
        if source_endpoint_settings is not None:
            self._values["source_endpoint_settings"] = source_endpoint_settings
        if target_endpoint_settings is not None:
            self._values["target_endpoint_settings"] = target_endpoint_settings
        if task_settings is not None:
            self._values["task_settings"] = task_settings

    @builtins.property
    def source_bucket_arn(self) -> builtins.str:
        '''The arn of the S3 bucket to be used as source.'''
        result = self._values.get("source_bucket_arn")
        assert result is not None, "Required property 'source_bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_mappings(self) -> "TableMappings":
        '''The table mappings to be used for the replication.'''
        result = self._values.get("table_mappings")
        assert result is not None, "Required property 'table_mappings' is missing"
        return typing.cast("TableMappings", result)

    @builtins.property
    def target_bucket_arn(self) -> builtins.str:
        '''The arn of the S3 bucket to be used as target.'''
        result = self._values.get("target_bucket_arn")
        assert result is not None, "Required property 'target_bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_endpoint_settings(self) -> typing.Optional["S3SourceEndpointSettings"]:
        '''The settings for the source s3 endpoint.'''
        result = self._values.get("source_endpoint_settings")
        return typing.cast(typing.Optional["S3SourceEndpointSettings"], result)

    @builtins.property
    def target_endpoint_settings(self) -> typing.Optional["S3TargetEndpointSettings"]:
        '''The settings for the source s3 endpoint.'''
        result = self._values.get("target_endpoint_settings")
        return typing.cast(typing.Optional["S3TargetEndpointSettings"], result)

    @builtins.property
    def task_settings(self) -> typing.Optional["TaskSettings"]:
        '''Optional JSON settings for AWS DMS Serverless replications.'''
        result = self._values.get("task_settings")
        return typing.cast(typing.Optional["TaskSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S32s3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="dms-patterns.S3DataType")
class S3DataType(enum.Enum):
    BYTE = "BYTE"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    INT1 = "INT1"
    INT2 = "INT2"
    INT4 = "INT4"
    INT8 = "INT8"
    NUMERIC = "NUMERIC"
    REAL4 = "REAL4"
    REAL8 = "REAL8"
    STRING = "STRING"
    UINT1 = "UINT1"
    UINT2 = "UINT2"
    UINT4 = "UINT4"
    UINT8 = "UINT8"
    BLOB = "BLOB"
    CLOB = "CLOB"
    BOOLEAN = "BOOLEAN"


class S3EndpointBase(
    _aws_cdk_aws_dms_ceddda9d.CfnEndpoint,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.S3EndpointBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_arn: builtins.str,
        endpoint_type: builtins.str,
        s3_settings: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnEndpoint.S3SettingsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_arn: The arn of the S3 bucket.
        :param endpoint_type: The type of endpoint.
        :param s3_settings: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cda125a2b8cad1fba43f8dfe14a0d6aad849dde17f4ef8251b166ee410d4284)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3EndpointBaseProps(
            bucket_arn=bucket_arn, endpoint_type=endpoint_type, s3_settings=s3_settings
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="dms-patterns.S3EndpointBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "endpoint_type": "endpointType",
        "s3_settings": "s3Settings",
    },
)
class S3EndpointBaseProps:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        endpoint_type: builtins.str,
        s3_settings: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnEndpoint.S3SettingsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_arn: The arn of the S3 bucket.
        :param endpoint_type: The type of endpoint.
        :param s3_settings: 
        '''
        if isinstance(s3_settings, dict):
            s3_settings = _aws_cdk_aws_dms_ceddda9d.CfnEndpoint.S3SettingsProperty(**s3_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae81c7a64e63f164c8dbdd9d5047c60d6fab0e86881186fe0f07199a06a1f6fe)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument s3_settings", value=s3_settings, expected_type=type_hints["s3_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "endpoint_type": endpoint_type,
        }
        if s3_settings is not None:
            self._values["s3_settings"] = s3_settings

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''The arn of the S3 bucket.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_type(self) -> builtins.str:
        '''The type of endpoint.'''
        result = self._values.get("endpoint_type")
        assert result is not None, "Required property 'endpoint_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_settings(
        self,
    ) -> typing.Optional[_aws_cdk_aws_dms_ceddda9d.CfnEndpoint.S3SettingsProperty]:
        result = self._values.get("s3_settings")
        return typing.cast(typing.Optional[_aws_cdk_aws_dms_ceddda9d.CfnEndpoint.S3SettingsProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3EndpointBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3Schema(metaclass=jsii.JSIIMeta, jsii_type="dms-patterns.S3Schema"):
    def __init__(
        self,
        tables: typing.Optional[typing.Sequence["Table"]] = None,
    ) -> None:
        '''
        :param tables: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e2430c2582bb2398d9d9a4e39ba076488d3b00379fa9636259d8e12085decf)
            check_type(argname="argument tables", value=tables, expected_type=type_hints["tables"])
        jsii.create(self.__class__, self, [tables])

    @jsii.member(jsii_name="addTable")
    def add_table(self, table: "Table") -> None:
        '''
        :param table: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0903cba4fa3dad8d7553474e3581f8d27ab8cb2d2db82293e6fbd64ea82091f5)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        return typing.cast(None, jsii.invoke(self, "addTable", [table]))

    @jsii.member(jsii_name="format")
    def format(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "format", []))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "toJSON", []))

    @builtins.property
    @jsii.member(jsii_name="tables")
    def tables(self) -> typing.List["Table"]:
        return typing.cast(typing.List["Table"], jsii.get(self, "tables"))

    @tables.setter
    def tables(self, value: typing.List["Table"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b526c8296db82e3b88e882a0e5c1e94ca144dccde76791364351d996361737be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tables", value)


class S3SourceEndpoint(
    S3EndpointBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.S3SourceEndpoint",
):
    '''An endpoint for a S3 source.

    This construct creates a role for DMS to access the S3 bucket.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_arn: builtins.str,
        s3_source_endpoint_settings: typing.Optional[typing.Union["S3SourceEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_arn: 
        :param s3_source_endpoint_settings: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f708c7afa5634d65010d037fffae9e36e9151974b7816d3b18e000aa09356f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3SourceEndpointProps(
            bucket_arn=bucket_arn,
            s3_source_endpoint_settings=s3_source_endpoint_settings,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="dms-patterns.S3SourceEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "s3_source_endpoint_settings": "s3SourceEndpointSettings",
    },
)
class S3SourceEndpointProps:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        s3_source_endpoint_settings: typing.Optional[typing.Union["S3SourceEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_arn: 
        :param s3_source_endpoint_settings: 
        '''
        if isinstance(s3_source_endpoint_settings, dict):
            s3_source_endpoint_settings = S3SourceEndpointSettings(**s3_source_endpoint_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae62b5d8f0195172abe7f4ff82655f7badf90962ac262914ed9736ed869f9e73)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument s3_source_endpoint_settings", value=s3_source_endpoint_settings, expected_type=type_hints["s3_source_endpoint_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
        }
        if s3_source_endpoint_settings is not None:
            self._values["s3_source_endpoint_settings"] = s3_source_endpoint_settings

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_source_endpoint_settings(
        self,
    ) -> typing.Optional["S3SourceEndpointSettings"]:
        result = self._values.get("s3_source_endpoint_settings")
        return typing.cast(typing.Optional["S3SourceEndpointSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3SourceEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="dms-patterns.S3SourceEndpointSettings",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_folder": "bucketFolder",
        "cdc_path": "cdcPath",
        "csv_delimiter": "csvDelimiter",
        "csv_null_value": "csvNullValue",
        "csv_row_delimiter": "csvRowDelimiter",
        "ignore_header_rows": "ignoreHeaderRows",
        "rfc4180": "rfc4180",
    },
)
class S3SourceEndpointSettings:
    def __init__(
        self,
        *,
        bucket_folder: typing.Optional[builtins.str] = None,
        cdc_path: typing.Optional[builtins.str] = None,
        csv_delimiter: typing.Optional[builtins.str] = None,
        csv_null_value: typing.Optional[builtins.str] = None,
        csv_row_delimiter: typing.Optional[builtins.str] = None,
        ignore_header_rows: typing.Optional[jsii.Number] = None,
        rfc4180: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_folder: An optional parameter to set a folder name in the S3 bucket. If provided, tables are created in the path ``*bucketFolder* / *schema_name* / *table_name* /`` . If this parameter isn't specified, the path used is ``*schema_name* / *table_name* /`` .
        :param cdc_path: Specifies the folder path of CDC files. For an S3 source, this setting is required if a task captures change data; otherwise, it's optional. If ``CdcPath`` is set, AWS DMS reads CDC files from this path and replicates the data changes to the target endpoint. For an S3 target if you set ```PreserveTransactions`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-PreserveTransactions>`_ to ``true`` , AWS DMS verifies that you have set this parameter to a folder path on your S3 target where AWS DMS can save the transaction order for the CDC load. AWS DMS creates this CDC folder path in either your S3 target working directory or the S3 target location specified by ```BucketFolder`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketFolder>`_ and ```BucketName`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketName>`_ . For example, if you specify ``CdcPath`` as ``MyChangedData`` , and you specify ``BucketName`` as ``MyTargetBucket`` but do not specify ``BucketFolder`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyChangedData`` . If you specify the same ``CdcPath`` , and you specify ``BucketName`` as ``MyTargetBucket`` and ``BucketFolder`` as ``MyTargetData`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyTargetData/MyChangedData`` . For more information on CDC including transaction order on an S3 target, see `Capturing data changes (CDC) including transaction order on the S3 target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.EndpointSettings.CdcPath>`_ . .. epigraph:: This setting is supported in AWS DMS versions 3.4.2 and later.
        :param csv_delimiter: The delimiter used to separate columns in the .csv file for both source and target. The default is a comma.
        :param csv_null_value: An optional parameter that specifies how AWS DMS treats null values. While handling the null value, you can use this parameter to pass a user-defined string as null when writing to the target. For example, when target columns are not nullable, you can use this option to differentiate between the empty string value and the null value. So, if you set this parameter value to the empty string ("" or ''), AWS DMS treats the empty string as the null value instead of ``NULL`` . The default value is ``NULL`` . Valid values include any valid string.
        :param csv_row_delimiter: The delimiter used to separate rows in the .csv file for both source and target. The default is a carriage return ( ``\\n`` ).
        :param ignore_header_rows: When this value is set to 1, AWS DMS ignores the first row header in a .csv file. A value of 1 turns on the feature; a value of 0 turns off the feature. The default is 0.
        :param rfc4180: For an S3 source, when this value is set to ``true`` or ``y`` , each leading double quotation mark has to be followed by an ending double quotation mark. This formatting complies with RFC 4180. When this value is set to ``false`` or ``n`` , string literals are copied to the target as is. In this case, a delimiter (row or column) signals the end of the field. Thus, you can't use a delimiter as part of the string, because it signals the end of the value. For an S3 target, an optional parameter used to set behavior to comply with RFC 4180 for data migrated to Amazon S3 using .csv file format only. When this value is set to ``true`` or ``y`` using Amazon S3 as a target, if the data has quotation marks or newline characters in it, AWS DMS encloses the entire column with an additional pair of double quotation marks ("). Every quotation mark within the data is repeated twice. The default value is ``true`` . Valid values include ``true`` , ``false`` , ``y`` , and ``n`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5472049b0881129ac75caae713086dd7faba23e150cfa7ee846b666dfc605290)
            check_type(argname="argument bucket_folder", value=bucket_folder, expected_type=type_hints["bucket_folder"])
            check_type(argname="argument cdc_path", value=cdc_path, expected_type=type_hints["cdc_path"])
            check_type(argname="argument csv_delimiter", value=csv_delimiter, expected_type=type_hints["csv_delimiter"])
            check_type(argname="argument csv_null_value", value=csv_null_value, expected_type=type_hints["csv_null_value"])
            check_type(argname="argument csv_row_delimiter", value=csv_row_delimiter, expected_type=type_hints["csv_row_delimiter"])
            check_type(argname="argument ignore_header_rows", value=ignore_header_rows, expected_type=type_hints["ignore_header_rows"])
            check_type(argname="argument rfc4180", value=rfc4180, expected_type=type_hints["rfc4180"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_folder is not None:
            self._values["bucket_folder"] = bucket_folder
        if cdc_path is not None:
            self._values["cdc_path"] = cdc_path
        if csv_delimiter is not None:
            self._values["csv_delimiter"] = csv_delimiter
        if csv_null_value is not None:
            self._values["csv_null_value"] = csv_null_value
        if csv_row_delimiter is not None:
            self._values["csv_row_delimiter"] = csv_row_delimiter
        if ignore_header_rows is not None:
            self._values["ignore_header_rows"] = ignore_header_rows
        if rfc4180 is not None:
            self._values["rfc4180"] = rfc4180

    @builtins.property
    def bucket_folder(self) -> typing.Optional[builtins.str]:
        '''An optional parameter to set a folder name in the S3 bucket.

        If provided, tables are created in the path ``*bucketFolder* / *schema_name* / *table_name* /`` . If this parameter isn't specified, the path used is ``*schema_name* / *table_name* /`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-bucketfolder
        '''
        result = self._values.get("bucket_folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdc_path(self) -> typing.Optional[builtins.str]:
        '''Specifies the folder path of CDC files.

        For an S3 source, this setting is required if a task captures change data; otherwise, it's optional. If ``CdcPath`` is set, AWS DMS reads CDC files from this path and replicates the data changes to the target endpoint. For an S3 target if you set ```PreserveTransactions`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-PreserveTransactions>`_ to ``true`` , AWS DMS verifies that you have set this parameter to a folder path on your S3 target where AWS DMS can save the transaction order for the CDC load. AWS DMS creates this CDC folder path in either your S3 target working directory or the S3 target location specified by ```BucketFolder`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketFolder>`_ and ```BucketName`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketName>`_ .

        For example, if you specify ``CdcPath`` as ``MyChangedData`` , and you specify ``BucketName`` as ``MyTargetBucket`` but do not specify ``BucketFolder`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyChangedData`` .

        If you specify the same ``CdcPath`` , and you specify ``BucketName`` as ``MyTargetBucket`` and ``BucketFolder`` as ``MyTargetData`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyTargetData/MyChangedData`` .

        For more information on CDC including transaction order on an S3 target, see `Capturing data changes (CDC) including transaction order on the S3 target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.EndpointSettings.CdcPath>`_ .
        .. epigraph::

           This setting is supported in AWS DMS versions 3.4.2 and later.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cdcpath
        '''
        result = self._values.get("cdc_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def csv_delimiter(self) -> typing.Optional[builtins.str]:
        '''The delimiter used to separate columns in the .csv file for both source and target. The default is a comma.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvdelimiter
        '''
        result = self._values.get("csv_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def csv_null_value(self) -> typing.Optional[builtins.str]:
        '''An optional parameter that specifies how AWS DMS treats null values.

        While handling the null value, you can use this parameter to pass a user-defined string as null when writing to the target. For example, when target columns are not nullable, you can use this option to differentiate between the empty string value and the null value. So, if you set this parameter value to the empty string ("" or ''), AWS DMS treats the empty string as the null value instead of ``NULL`` .

        The default value is ``NULL`` . Valid values include any valid string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvnullvalue
        '''
        result = self._values.get("csv_null_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def csv_row_delimiter(self) -> typing.Optional[builtins.str]:
        '''The delimiter used to separate rows in the .csv file for both source and target.

        The default is a carriage return ( ``\\n`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvrowdelimiter
        '''
        result = self._values.get("csv_row_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_header_rows(self) -> typing.Optional[jsii.Number]:
        '''When this value is set to 1, AWS DMS ignores the first row header in a .csv file. A value of 1 turns on the feature; a value of 0 turns off the feature.

        The default is 0.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-ignoreheaderrows
        '''
        result = self._values.get("ignore_header_rows")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rfc4180(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''For an S3 source, when this value is set to ``true`` or ``y`` , each leading double quotation mark has to be followed by an ending double quotation mark.

        This formatting complies with RFC 4180. When this value is set to ``false`` or ``n`` , string literals are copied to the target as is. In this case, a delimiter (row or column) signals the end of the field. Thus, you can't use a delimiter as part of the string, because it signals the end of the value.

        For an S3 target, an optional parameter used to set behavior to comply with RFC 4180 for data migrated to Amazon S3 using .csv file format only. When this value is set to ``true`` or ``y`` using Amazon S3 as a target, if the data has quotation marks or newline characters in it, AWS DMS encloses the entire column with an additional pair of double quotation marks ("). Every quotation mark within the data is repeated twice.

        The default value is ``true`` . Valid values include ``true`` , ``false`` , ``y`` , and ``n`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-rfc4180
        '''
        result = self._values.get("rfc4180")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3SourceEndpointSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3TargetEndpoint(
    S3EndpointBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.S3TargetEndpoint",
):
    '''An endpoint for a S3 target.

    This construct creates a role for DMS to access the S3 bucket.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_arn: builtins.str,
        s3_target_endpoint_settings: typing.Optional[typing.Union["S3TargetEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_arn: The arn of the target S3 bucket.
        :param s3_target_endpoint_settings: The settings for the target s3 endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444f504d5c7972ffde6e06307b69024cac924937bfc14a502cfae3dea1b853e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3TargetEndpointProps(
            bucket_arn=bucket_arn,
            s3_target_endpoint_settings=s3_target_endpoint_settings,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="dms-patterns.S3TargetEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "s3_target_endpoint_settings": "s3TargetEndpointSettings",
    },
)
class S3TargetEndpointProps:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        s3_target_endpoint_settings: typing.Optional[typing.Union["S3TargetEndpointSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_arn: The arn of the target S3 bucket.
        :param s3_target_endpoint_settings: The settings for the target s3 endpoint.
        '''
        if isinstance(s3_target_endpoint_settings, dict):
            s3_target_endpoint_settings = S3TargetEndpointSettings(**s3_target_endpoint_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a63d7889b615ad96536c4a307322f56a1d10c7105e3da1fd4ebd973e23ecc3)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument s3_target_endpoint_settings", value=s3_target_endpoint_settings, expected_type=type_hints["s3_target_endpoint_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
        }
        if s3_target_endpoint_settings is not None:
            self._values["s3_target_endpoint_settings"] = s3_target_endpoint_settings

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''The arn of the target S3 bucket.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_target_endpoint_settings(
        self,
    ) -> typing.Optional["S3TargetEndpointSettings"]:
        '''The settings for the target s3 endpoint.'''
        result = self._values.get("s3_target_endpoint_settings")
        return typing.cast(typing.Optional["S3TargetEndpointSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TargetEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="dms-patterns.S3TargetEndpointSettings",
    jsii_struct_bases=[],
    name_mapping={
        "add_column_name": "addColumnName",
        "bucket_folder": "bucketFolder",
        "canned_acl_for_objects": "cannedAclForObjects",
        "cdc_inserts_and_updates": "cdcInsertsAndUpdates",
        "cdc_inserts_only": "cdcInsertsOnly",
        "cdc_max_batch_interval": "cdcMaxBatchInterval",
        "cdc_min_file_size": "cdcMinFileSize",
        "cdc_path": "cdcPath",
        "compression_type": "compressionType",
        "csv_delimiter": "csvDelimiter",
        "csv_null_value": "csvNullValue",
        "csv_row_delimiter": "csvRowDelimiter",
        "data_format": "dataFormat",
        "data_page_size": "dataPageSize",
        "dict_page_size_limit": "dictPageSizeLimit",
        "enable_statistics": "enableStatistics",
        "encoding_type": "encodingType",
        "encryption_mode": "encryptionMode",
        "include_op_for_full_load": "includeOpForFullLoad",
        "max_file_size": "maxFileSize",
        "parquet_timestamp_in_millisecond": "parquetTimestampInMillisecond",
        "parquet_version": "parquetVersion",
        "preserve_transactions": "preserveTransactions",
        "rfc4180": "rfc4180",
        "row_group_length": "rowGroupLength",
        "server_side_encryption_kms_key_id": "serverSideEncryptionKmsKeyId",
        "timestamp_column_name": "timestampColumnName",
        "use_task_start_time_for_full_load_timestamp": "useTaskStartTimeForFullLoadTimestamp",
    },
)
class S3TargetEndpointSettings:
    def __init__(
        self,
        *,
        add_column_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        bucket_folder: typing.Optional[builtins.str] = None,
        canned_acl_for_objects: typing.Optional[builtins.str] = None,
        cdc_inserts_and_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        cdc_inserts_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        cdc_max_batch_interval: typing.Optional[jsii.Number] = None,
        cdc_min_file_size: typing.Optional[jsii.Number] = None,
        cdc_path: typing.Optional[builtins.str] = None,
        compression_type: typing.Optional[builtins.str] = None,
        csv_delimiter: typing.Optional[builtins.str] = None,
        csv_null_value: typing.Optional[builtins.str] = None,
        csv_row_delimiter: typing.Optional[builtins.str] = None,
        data_format: typing.Optional[builtins.str] = None,
        data_page_size: typing.Optional[jsii.Number] = None,
        dict_page_size_limit: typing.Optional[jsii.Number] = None,
        enable_statistics: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        encoding_type: typing.Optional[builtins.str] = None,
        encryption_mode: typing.Optional[builtins.str] = None,
        include_op_for_full_load: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        max_file_size: typing.Optional[jsii.Number] = None,
        parquet_timestamp_in_millisecond: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        parquet_version: typing.Optional[builtins.str] = None,
        preserve_transactions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        rfc4180: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        row_group_length: typing.Optional[jsii.Number] = None,
        server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
        timestamp_column_name: typing.Optional[builtins.str] = None,
        use_task_start_time_for_full_load_timestamp: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''
        :param add_column_name: An optional parameter that, when set to ``true`` or ``y`` , you can use to add column name information to the .csv output file. The default value is ``false`` . Valid values are ``true`` , ``false`` , ``y`` , and ``n`` .
        :param bucket_folder: An optional parameter to set a folder name in the S3 bucket. If provided, tables are created in the path ``*bucketFolder* / *schema_name* / *table_name* /`` . If this parameter isn't specified, the path used is ``*schema_name* / *table_name* /`` .
        :param canned_acl_for_objects: A value that enables AWS DMS to specify a predefined (canned) access control list (ACL) for objects created in an Amazon S3 bucket as .csv or .parquet files. For more information about Amazon S3 canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl>`_ in the *Amazon S3 Developer Guide* . The default value is NONE. Valid values include NONE, PRIVATE, PUBLIC_READ, PUBLIC_READ_WRITE, AUTHENTICATED_READ, AWS_EXEC_READ, BUCKET_OWNER_READ, and BUCKET_OWNER_FULL_CONTROL.
        :param cdc_inserts_and_updates: A value that enables a change data capture (CDC) load to write INSERT and UPDATE operations to .csv or .parquet (columnar storage) output files. The default setting is ``false`` , but when ``CdcInsertsAndUpdates`` is set to ``true`` or ``y`` , only INSERTs and UPDATEs from the source database are migrated to the .csv or .parquet file. For .csv file format only, how these INSERTs and UPDATEs are recorded depends on the value of the ``IncludeOpForFullLoad`` parameter. If ``IncludeOpForFullLoad`` is set to ``true`` , the first field of every CDC record is set to either ``I`` or ``U`` to indicate INSERT and UPDATE operations at the source. But if ``IncludeOpForFullLoad`` is set to ``false`` , CDC records are written without an indication of INSERT or UPDATE operations at the source. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* . .. epigraph:: AWS DMS supports the use of the ``CdcInsertsAndUpdates`` parameter in versions 3.3.1 and later. ``CdcInsertsOnly`` and ``CdcInsertsAndUpdates`` can't both be set to ``true`` for the same endpoint. Set either ``CdcInsertsOnly`` or ``CdcInsertsAndUpdates`` to ``true`` for the same endpoint, but not both.
        :param cdc_inserts_only: A value that enables a change data capture (CDC) load to write only INSERT operations to .csv or columnar storage (.parquet) output files. By default (the ``false`` setting), the first field in a .csv or .parquet record contains the letter I (INSERT), U (UPDATE), or D (DELETE). These values indicate whether the row was inserted, updated, or deleted at the source database for a CDC load to the target. If ``CdcInsertsOnly`` is set to ``true`` or ``y`` , only INSERTs from the source database are migrated to the .csv or .parquet file. For .csv format only, how these INSERTs are recorded depends on the value of ``IncludeOpForFullLoad`` . If ``IncludeOpForFullLoad`` is set to ``true`` , the first field of every CDC record is set to I to indicate the INSERT operation at the source. If ``IncludeOpForFullLoad`` is set to ``false`` , every CDC record is written without a first field to indicate the INSERT operation at the source. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* . .. epigraph:: AWS DMS supports the interaction described preceding between the ``CdcInsertsOnly`` and ``IncludeOpForFullLoad`` parameters in versions 3.1.4 and later. ``CdcInsertsOnly`` and ``CdcInsertsAndUpdates`` can't both be set to ``true`` for the same endpoint. Set either ``CdcInsertsOnly`` or ``CdcInsertsAndUpdates`` to ``true`` for the same endpoint, but not both.
        :param cdc_max_batch_interval: Maximum length of the interval, defined in seconds, after which to output a file to Amazon S3. When ``CdcMaxBatchInterval`` and ``CdcMinFileSize`` are both specified, the file write is triggered by whichever parameter condition is met first within an AWS DMS CloudFormation template. The default value is 60 seconds.
        :param cdc_min_file_size: Minimum file size, defined in kilobytes, to reach for a file output to Amazon S3. When ``CdcMinFileSize`` and ``CdcMaxBatchInterval`` are both specified, the file write is triggered by whichever parameter condition is met first within an AWS DMS CloudFormation template. The default value is 32 MB.
        :param cdc_path: Specifies the folder path of CDC files. For an S3 source, this setting is required if a task captures change data; otherwise, it's optional. If ``CdcPath`` is set, AWS DMS reads CDC files from this path and replicates the data changes to the target endpoint. For an S3 target if you set ```PreserveTransactions`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-PreserveTransactions>`_ to ``true`` , AWS DMS verifies that you have set this parameter to a folder path on your S3 target where AWS DMS can save the transaction order for the CDC load. AWS DMS creates this CDC folder path in either your S3 target working directory or the S3 target location specified by ```BucketFolder`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketFolder>`_ and ```BucketName`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketName>`_ . For example, if you specify ``CdcPath`` as ``MyChangedData`` , and you specify ``BucketName`` as ``MyTargetBucket`` but do not specify ``BucketFolder`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyChangedData`` . If you specify the same ``CdcPath`` , and you specify ``BucketName`` as ``MyTargetBucket`` and ``BucketFolder`` as ``MyTargetData`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyTargetData/MyChangedData`` . For more information on CDC including transaction order on an S3 target, see `Capturing data changes (CDC) including transaction order on the S3 target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.EndpointSettings.CdcPath>`_ . .. epigraph:: This setting is supported in AWS DMS versions 3.4.2 and later.
        :param compression_type: An optional parameter. When set to GZIP it enables the service to compress the target files. To allow the service to write the target files uncompressed, either set this parameter to NONE (the default) or don't specify the parameter at all. This parameter applies to both .csv and .parquet file formats.
        :param csv_delimiter: The delimiter used to separate columns in the .csv file for both source and target. The default is a comma.
        :param csv_null_value: An optional parameter that specifies how AWS DMS treats null values. While handling the null value, you can use this parameter to pass a user-defined string as null when writing to the target. For example, when target columns are not nullable, you can use this option to differentiate between the empty string value and the null value. So, if you set this parameter value to the empty string ("" or ''), AWS DMS treats the empty string as the null value instead of ``NULL`` . The default value is ``NULL`` . Valid values include any valid string.
        :param csv_row_delimiter: The delimiter used to separate rows in the .csv file for both source and target. The default is a carriage return ( ``\\n`` ).
        :param data_format: The format of the data that you want to use for output. You can choose one of the following:. - ``csv`` : This is a row-based file format with comma-separated values (.csv). - ``parquet`` : Apache Parquet (.parquet) is a columnar storage file format that features efficient compression and provides faster query response.
        :param data_page_size: The size of one data page in bytes. This parameter defaults to 1024 * 1024 bytes (1 MiB). This number is used for .parquet file format only.
        :param dict_page_size_limit: The maximum size of an encoded dictionary page of a column. If the dictionary page exceeds this, this column is stored using an encoding type of ``PLAIN`` . This parameter defaults to 1024 * 1024 bytes (1 MiB), the maximum size of a dictionary page before it reverts to ``PLAIN`` encoding. This size is used for .parquet file format only.
        :param enable_statistics: A value that enables statistics for Parquet pages and row groups. Choose ``true`` to enable statistics, ``false`` to disable. Statistics include ``NULL`` , ``DISTINCT`` , ``MAX`` , and ``MIN`` values. This parameter defaults to ``true`` . This value is used for .parquet file format only.
        :param encoding_type: The type of encoding that you're using:. - ``RLE_DICTIONARY`` uses a combination of bit-packing and run-length encoding to store repeated values more efficiently. This is the default. - ``PLAIN`` doesn't use encoding at all. Values are stored as they are. - ``PLAIN_DICTIONARY`` builds a dictionary of the values encountered in a given column. The dictionary is stored in a dictionary page for each column chunk.
        :param encryption_mode: The type of server-side encryption that you want to use for your data. This encryption type is part of the endpoint settings or the extra connections attributes for Amazon S3. You can choose either ``SSE_S3`` (the default) or ``SSE_KMS`` . .. epigraph:: For the ``ModifyEndpoint`` operation, you can change the existing value of the ``EncryptionMode`` parameter from ``SSE_KMS`` to ``SSE_S3`` . But you can’t change the existing value from ``SSE_S3`` to ``SSE_KMS`` . To use ``SSE_S3`` , create an AWS Identity and Access Management (IAM) role with a policy that allows ``"arn:aws:s3:::*"`` to use the following actions: ``"s3:PutObject", "s3:ListBucket"``
        :param include_op_for_full_load: A value that enables a full load to write INSERT operations to the comma-separated value (.csv) output files only to indicate how the rows were added to the source database. .. epigraph:: AWS DMS supports the ``IncludeOpForFullLoad`` parameter in versions 3.1.4 and later. For full load, records can only be inserted. By default (the ``false`` setting), no information is recorded in these output files for a full load to indicate that the rows were inserted at the source database. If ``IncludeOpForFullLoad`` is set to ``true`` or ``y`` , the INSERT is recorded as an I annotation in the first field of the .csv file. This allows the format of your target records from a full load to be consistent with the target records from a CDC load. .. epigraph:: This setting works together with the ``CdcInsertsOnly`` and the ``CdcInsertsAndUpdates`` parameters for output to .csv files only. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* .
        :param max_file_size: A value that specifies the maximum size (in KB) of any .csv file to be created while migrating to an S3 target during full load. The default value is 1,048,576 KB (1 GB). Valid values include 1 to 1,048,576.
        :param parquet_timestamp_in_millisecond: A value that specifies the precision of any ``TIMESTAMP`` column values that are written to an Amazon S3 object file in .parquet format. .. epigraph:: AWS DMS supports the ``ParquetTimestampInMillisecond`` parameter in versions 3.1.4 and later. When ``ParquetTimestampInMillisecond`` is set to ``true`` or ``y`` , AWS DMS writes all ``TIMESTAMP`` columns in a .parquet formatted file with millisecond precision. Otherwise, DMS writes them with microsecond precision. Currently, Amazon Athena and AWS Glue can handle only millisecond precision for ``TIMESTAMP`` values. Set this parameter to ``true`` for S3 endpoint object files that are .parquet formatted only if you plan to query or process the data with Athena or AWS Glue . .. epigraph:: AWS DMS writes any ``TIMESTAMP`` column values written to an S3 file in .csv format with microsecond precision. Setting ``ParquetTimestampInMillisecond`` has no effect on the string format of the timestamp column value that is inserted by setting the ``TimestampColumnName`` parameter.
        :param parquet_version: The version of the Apache Parquet format that you want to use: ``parquet_1_0`` (the default) or ``parquet_2_0`` .
        :param preserve_transactions: If this setting is set to ``true`` , AWS DMS saves the transaction order for a change data capture (CDC) load on the Amazon S3 target specified by ```CdcPath`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-CdcPath>`_ . For more information, see `Capturing data changes (CDC) including transaction order on the S3 target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.EndpointSettings.CdcPath>`_ . .. epigraph:: This setting is supported in AWS DMS versions 3.4.2 and later.
        :param rfc4180: For an S3 source, when this value is set to ``true`` or ``y`` , each leading double quotation mark has to be followed by an ending double quotation mark. This formatting complies with RFC 4180. When this value is set to ``false`` or ``n`` , string literals are copied to the target as is. In this case, a delimiter (row or column) signals the end of the field. Thus, you can't use a delimiter as part of the string, because it signals the end of the value. For an S3 target, an optional parameter used to set behavior to comply with RFC 4180 for data migrated to Amazon S3 using .csv file format only. When this value is set to ``true`` or ``y`` using Amazon S3 as a target, if the data has quotation marks or newline characters in it, AWS DMS encloses the entire column with an additional pair of double quotation marks ("). Every quotation mark within the data is repeated twice. The default value is ``true`` . Valid values include ``true`` , ``false`` , ``y`` , and ``n`` .
        :param row_group_length: The number of rows in a row group. A smaller row group size provides faster reads. But as the number of row groups grows, the slower writes become. This parameter defaults to 10,000 rows. This number is used for .parquet file format only. If you choose a value larger than the maximum, ``RowGroupLength`` is set to the max row group length in bytes (64 * 1024 * 1024).
        :param server_side_encryption_kms_key_id: The AWS KMS key ID. If you are using ``SSE_KMS`` for the ``EncryptionMode`` , provide this key ID. The key that you use needs an attached policy that enables IAM user permissions and allows use of the key.
        :param timestamp_column_name: A value that when nonblank causes AWS DMS to add a column with timestamp information to the endpoint data for an Amazon S3 target. .. epigraph:: AWS DMS supports the ``TimestampColumnName`` parameter in versions 3.1.4 and later. AWS DMS includes an additional ``STRING`` column in the .csv or .parquet object files of your migrated data when you set ``TimestampColumnName`` to a nonblank value. For a full load, each row of this timestamp column contains a timestamp for when the data was transferred from the source to the target by DMS. For a change data capture (CDC) load, each row of the timestamp column contains the timestamp for the commit of that row in the source database. The string format for this timestamp column value is ``yyyy-MM-dd HH:mm:ss.SSSSSS`` . By default, the precision of this value is in microseconds. For a CDC load, the rounding of the precision depends on the commit timestamp supported by DMS for the source database. When the ``AddColumnName`` parameter is set to ``true`` , DMS also includes a name for the timestamp column that you set with ``TimestampColumnName`` .
        :param use_task_start_time_for_full_load_timestamp: When set to true, this parameter uses the task start time as the timestamp column value instead of the time data is written to target. For full load, when ``useTaskStartTimeForFullLoadTimestamp`` is set to ``true`` , each row of the timestamp column contains the task start time. For CDC loads, each row of the timestamp column contains the transaction commit time. When ``useTaskStartTimeForFullLoadTimestamp`` is set to ``false`` , the full load timestamp in the timestamp column increments with the time data arrives at the target.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13aa07b3157ed245b02c419e68a9056b33fd7059a8975452dcb4b768e0417a6)
            check_type(argname="argument add_column_name", value=add_column_name, expected_type=type_hints["add_column_name"])
            check_type(argname="argument bucket_folder", value=bucket_folder, expected_type=type_hints["bucket_folder"])
            check_type(argname="argument canned_acl_for_objects", value=canned_acl_for_objects, expected_type=type_hints["canned_acl_for_objects"])
            check_type(argname="argument cdc_inserts_and_updates", value=cdc_inserts_and_updates, expected_type=type_hints["cdc_inserts_and_updates"])
            check_type(argname="argument cdc_inserts_only", value=cdc_inserts_only, expected_type=type_hints["cdc_inserts_only"])
            check_type(argname="argument cdc_max_batch_interval", value=cdc_max_batch_interval, expected_type=type_hints["cdc_max_batch_interval"])
            check_type(argname="argument cdc_min_file_size", value=cdc_min_file_size, expected_type=type_hints["cdc_min_file_size"])
            check_type(argname="argument cdc_path", value=cdc_path, expected_type=type_hints["cdc_path"])
            check_type(argname="argument compression_type", value=compression_type, expected_type=type_hints["compression_type"])
            check_type(argname="argument csv_delimiter", value=csv_delimiter, expected_type=type_hints["csv_delimiter"])
            check_type(argname="argument csv_null_value", value=csv_null_value, expected_type=type_hints["csv_null_value"])
            check_type(argname="argument csv_row_delimiter", value=csv_row_delimiter, expected_type=type_hints["csv_row_delimiter"])
            check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
            check_type(argname="argument data_page_size", value=data_page_size, expected_type=type_hints["data_page_size"])
            check_type(argname="argument dict_page_size_limit", value=dict_page_size_limit, expected_type=type_hints["dict_page_size_limit"])
            check_type(argname="argument enable_statistics", value=enable_statistics, expected_type=type_hints["enable_statistics"])
            check_type(argname="argument encoding_type", value=encoding_type, expected_type=type_hints["encoding_type"])
            check_type(argname="argument encryption_mode", value=encryption_mode, expected_type=type_hints["encryption_mode"])
            check_type(argname="argument include_op_for_full_load", value=include_op_for_full_load, expected_type=type_hints["include_op_for_full_load"])
            check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
            check_type(argname="argument parquet_timestamp_in_millisecond", value=parquet_timestamp_in_millisecond, expected_type=type_hints["parquet_timestamp_in_millisecond"])
            check_type(argname="argument parquet_version", value=parquet_version, expected_type=type_hints["parquet_version"])
            check_type(argname="argument preserve_transactions", value=preserve_transactions, expected_type=type_hints["preserve_transactions"])
            check_type(argname="argument rfc4180", value=rfc4180, expected_type=type_hints["rfc4180"])
            check_type(argname="argument row_group_length", value=row_group_length, expected_type=type_hints["row_group_length"])
            check_type(argname="argument server_side_encryption_kms_key_id", value=server_side_encryption_kms_key_id, expected_type=type_hints["server_side_encryption_kms_key_id"])
            check_type(argname="argument timestamp_column_name", value=timestamp_column_name, expected_type=type_hints["timestamp_column_name"])
            check_type(argname="argument use_task_start_time_for_full_load_timestamp", value=use_task_start_time_for_full_load_timestamp, expected_type=type_hints["use_task_start_time_for_full_load_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_column_name is not None:
            self._values["add_column_name"] = add_column_name
        if bucket_folder is not None:
            self._values["bucket_folder"] = bucket_folder
        if canned_acl_for_objects is not None:
            self._values["canned_acl_for_objects"] = canned_acl_for_objects
        if cdc_inserts_and_updates is not None:
            self._values["cdc_inserts_and_updates"] = cdc_inserts_and_updates
        if cdc_inserts_only is not None:
            self._values["cdc_inserts_only"] = cdc_inserts_only
        if cdc_max_batch_interval is not None:
            self._values["cdc_max_batch_interval"] = cdc_max_batch_interval
        if cdc_min_file_size is not None:
            self._values["cdc_min_file_size"] = cdc_min_file_size
        if cdc_path is not None:
            self._values["cdc_path"] = cdc_path
        if compression_type is not None:
            self._values["compression_type"] = compression_type
        if csv_delimiter is not None:
            self._values["csv_delimiter"] = csv_delimiter
        if csv_null_value is not None:
            self._values["csv_null_value"] = csv_null_value
        if csv_row_delimiter is not None:
            self._values["csv_row_delimiter"] = csv_row_delimiter
        if data_format is not None:
            self._values["data_format"] = data_format
        if data_page_size is not None:
            self._values["data_page_size"] = data_page_size
        if dict_page_size_limit is not None:
            self._values["dict_page_size_limit"] = dict_page_size_limit
        if enable_statistics is not None:
            self._values["enable_statistics"] = enable_statistics
        if encoding_type is not None:
            self._values["encoding_type"] = encoding_type
        if encryption_mode is not None:
            self._values["encryption_mode"] = encryption_mode
        if include_op_for_full_load is not None:
            self._values["include_op_for_full_load"] = include_op_for_full_load
        if max_file_size is not None:
            self._values["max_file_size"] = max_file_size
        if parquet_timestamp_in_millisecond is not None:
            self._values["parquet_timestamp_in_millisecond"] = parquet_timestamp_in_millisecond
        if parquet_version is not None:
            self._values["parquet_version"] = parquet_version
        if preserve_transactions is not None:
            self._values["preserve_transactions"] = preserve_transactions
        if rfc4180 is not None:
            self._values["rfc4180"] = rfc4180
        if row_group_length is not None:
            self._values["row_group_length"] = row_group_length
        if server_side_encryption_kms_key_id is not None:
            self._values["server_side_encryption_kms_key_id"] = server_side_encryption_kms_key_id
        if timestamp_column_name is not None:
            self._values["timestamp_column_name"] = timestamp_column_name
        if use_task_start_time_for_full_load_timestamp is not None:
            self._values["use_task_start_time_for_full_load_timestamp"] = use_task_start_time_for_full_load_timestamp

    @builtins.property
    def add_column_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''An optional parameter that, when set to ``true`` or ``y`` , you can use to add column name information to the .csv output file.

        The default value is ``false`` . Valid values are ``true`` , ``false`` , ``y`` , and ``n`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-addcolumnname
        '''
        result = self._values.get("add_column_name")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def bucket_folder(self) -> typing.Optional[builtins.str]:
        '''An optional parameter to set a folder name in the S3 bucket.

        If provided, tables are created in the path ``*bucketFolder* / *schema_name* / *table_name* /`` . If this parameter isn't specified, the path used is ``*schema_name* / *table_name* /`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-bucketfolder
        '''
        result = self._values.get("bucket_folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def canned_acl_for_objects(self) -> typing.Optional[builtins.str]:
        '''A value that enables AWS DMS to specify a predefined (canned) access control list (ACL) for objects created in an Amazon S3 bucket as .csv or .parquet files. For more information about Amazon S3 canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl>`_ in the *Amazon S3 Developer Guide* .

        The default value is NONE. Valid values include NONE, PRIVATE, PUBLIC_READ, PUBLIC_READ_WRITE, AUTHENTICATED_READ, AWS_EXEC_READ, BUCKET_OWNER_READ, and BUCKET_OWNER_FULL_CONTROL.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cannedaclforobjects
        '''
        result = self._values.get("canned_acl_for_objects")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdc_inserts_and_updates(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that enables a change data capture (CDC) load to write INSERT and UPDATE operations to .csv or .parquet (columnar storage) output files. The default setting is ``false`` , but when ``CdcInsertsAndUpdates`` is set to ``true`` or ``y`` , only INSERTs and UPDATEs from the source database are migrated to the .csv or .parquet file.

        For .csv file format only, how these INSERTs and UPDATEs are recorded depends on the value of the ``IncludeOpForFullLoad`` parameter. If ``IncludeOpForFullLoad`` is set to ``true`` , the first field of every CDC record is set to either ``I`` or ``U`` to indicate INSERT and UPDATE operations at the source. But if ``IncludeOpForFullLoad`` is set to ``false`` , CDC records are written without an indication of INSERT or UPDATE operations at the source. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* .
        .. epigraph::

           AWS DMS supports the use of the ``CdcInsertsAndUpdates`` parameter in versions 3.3.1 and later.

           ``CdcInsertsOnly`` and ``CdcInsertsAndUpdates`` can't both be set to ``true`` for the same endpoint. Set either ``CdcInsertsOnly`` or ``CdcInsertsAndUpdates`` to ``true`` for the same endpoint, but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cdcinsertsandupdates
        '''
        result = self._values.get("cdc_inserts_and_updates")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def cdc_inserts_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that enables a change data capture (CDC) load to write only INSERT operations to .csv or columnar storage (.parquet) output files. By default (the ``false`` setting), the first field in a .csv or .parquet record contains the letter I (INSERT), U (UPDATE), or D (DELETE). These values indicate whether the row was inserted, updated, or deleted at the source database for a CDC load to the target.

        If ``CdcInsertsOnly`` is set to ``true`` or ``y`` , only INSERTs from the source database are migrated to the .csv or .parquet file. For .csv format only, how these INSERTs are recorded depends on the value of ``IncludeOpForFullLoad`` . If ``IncludeOpForFullLoad`` is set to ``true`` , the first field of every CDC record is set to I to indicate the INSERT operation at the source. If ``IncludeOpForFullLoad`` is set to ``false`` , every CDC record is written without a first field to indicate the INSERT operation at the source. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* .
        .. epigraph::

           AWS DMS supports the interaction described preceding between the ``CdcInsertsOnly`` and ``IncludeOpForFullLoad`` parameters in versions 3.1.4 and later.

           ``CdcInsertsOnly`` and ``CdcInsertsAndUpdates`` can't both be set to ``true`` for the same endpoint. Set either ``CdcInsertsOnly`` or ``CdcInsertsAndUpdates`` to ``true`` for the same endpoint, but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cdcinsertsonly
        '''
        result = self._values.get("cdc_inserts_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def cdc_max_batch_interval(self) -> typing.Optional[jsii.Number]:
        '''Maximum length of the interval, defined in seconds, after which to output a file to Amazon S3.

        When ``CdcMaxBatchInterval`` and ``CdcMinFileSize`` are both specified, the file write is triggered by whichever parameter condition is met first within an AWS DMS CloudFormation template.

        The default value is 60 seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cdcmaxbatchinterval
        '''
        result = self._values.get("cdc_max_batch_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cdc_min_file_size(self) -> typing.Optional[jsii.Number]:
        '''Minimum file size, defined in kilobytes, to reach for a file output to Amazon S3.

        When ``CdcMinFileSize`` and ``CdcMaxBatchInterval`` are both specified, the file write is triggered by whichever parameter condition is met first within an AWS DMS CloudFormation template.

        The default value is 32 MB.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cdcminfilesize
        '''
        result = self._values.get("cdc_min_file_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cdc_path(self) -> typing.Optional[builtins.str]:
        '''Specifies the folder path of CDC files.

        For an S3 source, this setting is required if a task captures change data; otherwise, it's optional. If ``CdcPath`` is set, AWS DMS reads CDC files from this path and replicates the data changes to the target endpoint. For an S3 target if you set ```PreserveTransactions`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-PreserveTransactions>`_ to ``true`` , AWS DMS verifies that you have set this parameter to a folder path on your S3 target where AWS DMS can save the transaction order for the CDC load. AWS DMS creates this CDC folder path in either your S3 target working directory or the S3 target location specified by ```BucketFolder`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketFolder>`_ and ```BucketName`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-BucketName>`_ .

        For example, if you specify ``CdcPath`` as ``MyChangedData`` , and you specify ``BucketName`` as ``MyTargetBucket`` but do not specify ``BucketFolder`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyChangedData`` .

        If you specify the same ``CdcPath`` , and you specify ``BucketName`` as ``MyTargetBucket`` and ``BucketFolder`` as ``MyTargetData`` , AWS DMS creates the CDC folder path following: ``MyTargetBucket/MyTargetData/MyChangedData`` .

        For more information on CDC including transaction order on an S3 target, see `Capturing data changes (CDC) including transaction order on the S3 target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.EndpointSettings.CdcPath>`_ .
        .. epigraph::

           This setting is supported in AWS DMS versions 3.4.2 and later.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-cdcpath
        '''
        result = self._values.get("cdc_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_type(self) -> typing.Optional[builtins.str]:
        '''An optional parameter.

        When set to GZIP it enables the service to compress the target files. To allow the service to write the target files uncompressed, either set this parameter to NONE (the default) or don't specify the parameter at all. This parameter applies to both .csv and .parquet file formats.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-compressiontype
        '''
        result = self._values.get("compression_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def csv_delimiter(self) -> typing.Optional[builtins.str]:
        '''The delimiter used to separate columns in the .csv file for both source and target. The default is a comma.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvdelimiter
        '''
        result = self._values.get("csv_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def csv_null_value(self) -> typing.Optional[builtins.str]:
        '''An optional parameter that specifies how AWS DMS treats null values.

        While handling the null value, you can use this parameter to pass a user-defined string as null when writing to the target. For example, when target columns are not nullable, you can use this option to differentiate between the empty string value and the null value. So, if you set this parameter value to the empty string ("" or ''), AWS DMS treats the empty string as the null value instead of ``NULL`` .

        The default value is ``NULL`` . Valid values include any valid string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvnullvalue
        '''
        result = self._values.get("csv_null_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def csv_row_delimiter(self) -> typing.Optional[builtins.str]:
        '''The delimiter used to separate rows in the .csv file for both source and target.

        The default is a carriage return ( ``\\n`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvrowdelimiter
        '''
        result = self._values.get("csv_row_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_format(self) -> typing.Optional[builtins.str]:
        '''The format of the data that you want to use for output. You can choose one of the following:.

        - ``csv`` : This is a row-based file format with comma-separated values (.csv).
        - ``parquet`` : Apache Parquet (.parquet) is a columnar storage file format that features efficient compression and provides faster query response.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-dataformat
        '''
        result = self._values.get("data_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_page_size(self) -> typing.Optional[jsii.Number]:
        '''The size of one data page in bytes.

        This parameter defaults to 1024 * 1024 bytes (1 MiB). This number is used for .parquet file format only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-datapagesize
        '''
        result = self._values.get("data_page_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dict_page_size_limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum size of an encoded dictionary page of a column.

        If the dictionary page exceeds this, this column is stored using an encoding type of ``PLAIN`` . This parameter defaults to 1024 * 1024 bytes (1 MiB), the maximum size of a dictionary page before it reverts to ``PLAIN`` encoding. This size is used for .parquet file format only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-dictpagesizelimit
        '''
        result = self._values.get("dict_page_size_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_statistics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that enables statistics for Parquet pages and row groups.

        Choose ``true`` to enable statistics, ``false`` to disable. Statistics include ``NULL`` , ``DISTINCT`` , ``MAX`` , and ``MIN`` values. This parameter defaults to ``true`` . This value is used for .parquet file format only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-enablestatistics
        '''
        result = self._values.get("enable_statistics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def encoding_type(self) -> typing.Optional[builtins.str]:
        '''The type of encoding that you're using:.

        - ``RLE_DICTIONARY`` uses a combination of bit-packing and run-length encoding to store repeated values more efficiently. This is the default.
        - ``PLAIN`` doesn't use encoding at all. Values are stored as they are.
        - ``PLAIN_DICTIONARY`` builds a dictionary of the values encountered in a given column. The dictionary is stored in a dictionary page for each column chunk.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-encodingtype
        '''
        result = self._values.get("encoding_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_mode(self) -> typing.Optional[builtins.str]:
        '''The type of server-side encryption that you want to use for your data.

        This encryption type is part of the endpoint settings or the extra connections attributes for Amazon S3. You can choose either ``SSE_S3`` (the default) or ``SSE_KMS`` .
        .. epigraph::

           For the ``ModifyEndpoint`` operation, you can change the existing value of the ``EncryptionMode`` parameter from ``SSE_KMS`` to ``SSE_S3`` . But you can’t change the existing value from ``SSE_S3`` to ``SSE_KMS`` .

        To use ``SSE_S3`` , create an AWS Identity and Access Management (IAM) role with a policy that allows ``"arn:aws:s3:::*"`` to use the following actions: ``"s3:PutObject", "s3:ListBucket"``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-encryptionmode
        '''
        result = self._values.get("encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_op_for_full_load(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that enables a full load to write INSERT operations to the comma-separated value (.csv) output files only to indicate how the rows were added to the source database.

        .. epigraph::

           AWS DMS supports the ``IncludeOpForFullLoad`` parameter in versions 3.1.4 and later.

        For full load, records can only be inserted. By default (the ``false`` setting), no information is recorded in these output files for a full load to indicate that the rows were inserted at the source database. If ``IncludeOpForFullLoad`` is set to ``true`` or ``y`` , the INSERT is recorded as an I annotation in the first field of the .csv file. This allows the format of your target records from a full load to be consistent with the target records from a CDC load.
        .. epigraph::

           This setting works together with the ``CdcInsertsOnly`` and the ``CdcInsertsAndUpdates`` parameters for output to .csv files only. For more information about how these settings work together, see `Indicating Source DB Operations in Migrated S3 Data <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring.InsertOps>`_ in the *AWS Database Migration Service User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-includeopforfullload
        '''
        result = self._values.get("include_op_for_full_load")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def max_file_size(self) -> typing.Optional[jsii.Number]:
        '''A value that specifies the maximum size (in KB) of any .csv file to be created while migrating to an S3 target during full load.

        The default value is 1,048,576 KB (1 GB). Valid values include 1 to 1,048,576.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-maxfilesize
        '''
        result = self._values.get("max_file_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def parquet_timestamp_in_millisecond(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that specifies the precision of any ``TIMESTAMP`` column values that are written to an Amazon S3 object file in .parquet format.

        .. epigraph::

           AWS DMS supports the ``ParquetTimestampInMillisecond`` parameter in versions 3.1.4 and later.

        When ``ParquetTimestampInMillisecond`` is set to ``true`` or ``y`` , AWS DMS writes all ``TIMESTAMP`` columns in a .parquet formatted file with millisecond precision. Otherwise, DMS writes them with microsecond precision.

        Currently, Amazon Athena and AWS Glue can handle only millisecond precision for ``TIMESTAMP`` values. Set this parameter to ``true`` for S3 endpoint object files that are .parquet formatted only if you plan to query or process the data with Athena or AWS Glue .
        .. epigraph::

           AWS DMS writes any ``TIMESTAMP`` column values written to an S3 file in .csv format with microsecond precision.

           Setting ``ParquetTimestampInMillisecond`` has no effect on the string format of the timestamp column value that is inserted by setting the ``TimestampColumnName`` parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-parquettimestampinmillisecond
        '''
        result = self._values.get("parquet_timestamp_in_millisecond")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def parquet_version(self) -> typing.Optional[builtins.str]:
        '''The version of the Apache Parquet format that you want to use: ``parquet_1_0`` (the default) or ``parquet_2_0`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-parquetversion
        '''
        result = self._values.get("parquet_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserve_transactions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If this setting is set to ``true`` , AWS DMS saves the transaction order for a change data capture (CDC) load on the Amazon S3 target specified by ```CdcPath`` <https://docs.aws.amazon.com/dms/latest/APIReference/API_S3Settings.html#DMS-Type-S3Settings-CdcPath>`_ . For more information, see `Capturing data changes (CDC) including transaction order on the S3 target <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.EndpointSettings.CdcPath>`_ .

        .. epigraph::

           This setting is supported in AWS DMS versions 3.4.2 and later.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-preservetransactions
        '''
        result = self._values.get("preserve_transactions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def rfc4180(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''For an S3 source, when this value is set to ``true`` or ``y`` , each leading double quotation mark has to be followed by an ending double quotation mark.

        This formatting complies with RFC 4180. When this value is set to ``false`` or ``n`` , string literals are copied to the target as is. In this case, a delimiter (row or column) signals the end of the field. Thus, you can't use a delimiter as part of the string, because it signals the end of the value.

        For an S3 target, an optional parameter used to set behavior to comply with RFC 4180 for data migrated to Amazon S3 using .csv file format only. When this value is set to ``true`` or ``y`` using Amazon S3 as a target, if the data has quotation marks or newline characters in it, AWS DMS encloses the entire column with an additional pair of double quotation marks ("). Every quotation mark within the data is repeated twice.

        The default value is ``true`` . Valid values include ``true`` , ``false`` , ``y`` , and ``n`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-rfc4180
        '''
        result = self._values.get("rfc4180")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def row_group_length(self) -> typing.Optional[jsii.Number]:
        '''The number of rows in a row group.

        A smaller row group size provides faster reads. But as the number of row groups grows, the slower writes become. This parameter defaults to 10,000 rows. This number is used for .parquet file format only.

        If you choose a value larger than the maximum, ``RowGroupLength`` is set to the max row group length in bytes (64 * 1024 * 1024).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-rowgrouplength
        '''
        result = self._values.get("row_group_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def server_side_encryption_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS KMS key ID.

        If you are using ``SSE_KMS`` for the ``EncryptionMode`` , provide this key ID. The key that you use needs an attached policy that enables IAM user permissions and allows use of the key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-redshiftsettings.html#cfn-dms-endpoint-redshiftsettings-serversideencryptionkmskeyid
        '''
        result = self._values.get("server_side_encryption_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_column_name(self) -> typing.Optional[builtins.str]:
        '''A value that when nonblank causes AWS DMS to add a column with timestamp information to the endpoint data for an Amazon S3 target.

        .. epigraph::

           AWS DMS supports the ``TimestampColumnName`` parameter in versions 3.1.4 and later.

        AWS DMS includes an additional ``STRING`` column in the .csv or .parquet object files of your migrated data when you set ``TimestampColumnName`` to a nonblank value.

        For a full load, each row of this timestamp column contains a timestamp for when the data was transferred from the source to the target by DMS.

        For a change data capture (CDC) load, each row of the timestamp column contains the timestamp for the commit of that row in the source database.

        The string format for this timestamp column value is ``yyyy-MM-dd HH:mm:ss.SSSSSS`` . By default, the precision of this value is in microseconds. For a CDC load, the rounding of the precision depends on the commit timestamp supported by DMS for the source database.

        When the ``AddColumnName`` parameter is set to ``true`` , DMS also includes a name for the timestamp column that you set with ``TimestampColumnName`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-timestampcolumnname
        '''
        result = self._values.get("timestamp_column_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_task_start_time_for_full_load_timestamp(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When set to true, this parameter uses the task start time as the timestamp column value instead of the time data is written to target.

        For full load, when ``useTaskStartTimeForFullLoadTimestamp`` is set to ``true`` , each row of the timestamp column contains the task start time. For CDC loads, each row of the timestamp column contains the transaction commit time.

        When ``useTaskStartTimeForFullLoadTimestamp`` is set to ``false`` , the full load timestamp in the timestamp column increments with the time data arrives at the target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-usetaskstarttimeforfullloadtimestamp
        '''
        result = self._values.get("use_task_start_time_for_full_load_timestamp")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TargetEndpointSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="dms-patterns.SelectionAction")
class SelectionAction(enum.Enum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"
    EXPLICIT = "EXPLICIT"


@jsii.data_type(
    jsii_type="dms-patterns.SelectionObjectLocator",
    jsii_struct_bases=[ObjectLocator],
    name_mapping={
        "schema_name": "schemaName",
        "table_name": "tableName",
        "table_type": "tableType",
    },
)
class SelectionObjectLocator(ObjectLocator):
    def __init__(
        self,
        *,
        schema_name: builtins.str,
        table_name: typing.Optional[builtins.str] = None,
        table_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_name: 
        :param table_name: 
        :param table_type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ea00ab8131194666102cb41f06317a4eae504ec9438de5b78509f1d9a02b9d)
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument table_type", value=table_type, expected_type=type_hints["table_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema_name": schema_name,
        }
        if table_name is not None:
            self._values["table_name"] = table_name
        if table_type is not None:
            self._values["table_type"] = table_type

    @builtins.property
    def schema_name(self) -> builtins.str:
        result = self._values.get("schema_name")
        assert result is not None, "Required property 'schema_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SelectionObjectLocator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SelectionRule(
    Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.SelectionRule",
):
    def __init__(
        self,
        *,
        object_locator: typing.Union[SelectionObjectLocator, typing.Dict[builtins.str, typing.Any]],
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        load_order: typing.Optional[jsii.Number] = None,
        rule_action: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_locator: 
        :param filters: 
        :param load_order: 
        :param rule_action: 
        :param rule_id: 
        :param rule_name: 
        '''
        props = SelectionRuleProps(
            object_locator=object_locator,
            filters=filters,
            load_order=load_order,
            rule_action=rule_action,
            rule_id=rule_id,
            rule_name=rule_name,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="format")
    def format(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "format", []))

    @builtins.property
    @jsii.member(jsii_name="objectLocator")
    def object_locator(self) -> SelectionObjectLocator:
        return typing.cast(SelectionObjectLocator, jsii.get(self, "objectLocator"))

    @object_locator.setter
    def object_locator(self, value: SelectionObjectLocator) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b10ee67f01cd5b29d311598ec587c0f59ddbc66499745b9032abb8c35d115e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectLocator", value)

    @builtins.property
    @jsii.member(jsii_name="ruleType")
    def rule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleType"))

    @rule_type.setter
    def rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c03d3c6f0e2d06c6c46b2b375e6148d0b4c2ed1f2ee5c71017500e5e9811a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleType", value)

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        return typing.cast(typing.Optional[typing.List[typing.Any]], jsii.get(self, "filters"))

    @filters.setter
    def filters(self, value: typing.Optional[typing.List[typing.Any]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e930f6f98ef8924df1fd35c2dad91a1eb8aebf230ef829e26a85b641af217ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filters", value)

    @builtins.property
    @jsii.member(jsii_name="loadOrder")
    def load_order(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "loadOrder"))

    @load_order.setter
    def load_order(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b817073504973077b206c43b1254f2161c4774b5eddb65ec8a031c2de3674ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadOrder", value)


@jsii.data_type(
    jsii_type="dms-patterns.SelectionRuleProps",
    jsii_struct_bases=[RuleProps],
    name_mapping={
        "filters": "filters",
        "load_order": "loadOrder",
        "rule_action": "ruleAction",
        "rule_id": "ruleId",
        "rule_name": "ruleName",
        "object_locator": "objectLocator",
    },
)
class SelectionRuleProps(RuleProps):
    def __init__(
        self,
        *,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        load_order: typing.Optional[jsii.Number] = None,
        rule_action: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
        object_locator: typing.Union[SelectionObjectLocator, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param filters: 
        :param load_order: 
        :param rule_action: 
        :param rule_id: 
        :param rule_name: 
        :param object_locator: 
        '''
        if isinstance(object_locator, dict):
            object_locator = SelectionObjectLocator(**object_locator)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7224a7df496e4ec105599c7b7ea2a2dfc92554bf69f5f9b690b599c7e1cbd3)
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument load_order", value=load_order, expected_type=type_hints["load_order"])
            check_type(argname="argument rule_action", value=rule_action, expected_type=type_hints["rule_action"])
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument object_locator", value=object_locator, expected_type=type_hints["object_locator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_locator": object_locator,
        }
        if filters is not None:
            self._values["filters"] = filters
        if load_order is not None:
            self._values["load_order"] = load_order
        if rule_action is not None:
            self._values["rule_action"] = rule_action
        if rule_id is not None:
            self._values["rule_id"] = rule_id
        if rule_name is not None:
            self._values["rule_name"] = rule_name

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def load_order(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("load_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rule_action(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_locator(self) -> SelectionObjectLocator:
        result = self._values.get("object_locator")
        assert result is not None, "Required property 'object_locator' is missing"
        return typing.cast(SelectionObjectLocator, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SelectionRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Table(metaclass=jsii.JSIIMeta, jsii_type="dms-patterns.Table"):
    def __init__(
        self,
        *,
        table_columns: typing.Sequence["TableColumn"],
        table_name: builtins.str,
        table_owner: builtins.str,
        table_path: builtins.str,
    ) -> None:
        '''
        :param table_columns: 
        :param table_name: 
        :param table_owner: 
        :param table_path: 
        '''
        props = TableProps(
            table_columns=table_columns,
            table_name=table_name,
            table_owner=table_owner,
            table_path=table_path,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="format")
    def format(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "format", []))

    @builtins.property
    @jsii.member(jsii_name="tableColumns")
    def table_columns(self) -> typing.List["TableColumn"]:
        return typing.cast(typing.List["TableColumn"], jsii.get(self, "tableColumns"))

    @table_columns.setter
    def table_columns(self, value: typing.List["TableColumn"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5880519a9b236d385ff5105ca351a9d728d4c60c44b17f1b2375ed313bcd5deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableColumns", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9350ff38a946b7c1c9cc58e210806a96a1598c2546fb4e41e75cc477ba84afcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value)

    @builtins.property
    @jsii.member(jsii_name="tableOwner")
    def table_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableOwner"))

    @table_owner.setter
    def table_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04225f5d3257db1c0e410713e3c71b79525bcf331f8af533d65e7ef0b3f20f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableOwner", value)

    @builtins.property
    @jsii.member(jsii_name="tablePath")
    def table_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tablePath"))

    @table_path.setter
    def table_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10182c6f41621b1ebdb03e47a49272785affdbb4e191ef96afc37087f5f01a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tablePath", value)


class TableColumn(metaclass=jsii.JSIIMeta, jsii_type="dms-patterns.TableColumn"):
    def __init__(
        self,
        *,
        column_name: builtins.str,
        column_type: S3DataType,
        column_date_format: typing.Optional[builtins.str] = None,
        column_is_pk: typing.Optional[builtins.bool] = None,
        column_length: typing.Optional[jsii.Number] = None,
        column_nullable: typing.Optional[builtins.bool] = None,
        column_precision: typing.Optional[jsii.Number] = None,
        column_scale: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column_name: 
        :param column_type: 
        :param column_date_format: 
        :param column_is_pk: 
        :param column_length: 
        :param column_nullable: 
        :param column_precision: 
        :param column_scale: 
        '''
        props = TableColumnProps(
            column_name=column_name,
            column_type=column_type,
            column_date_format=column_date_format,
            column_is_pk=column_is_pk,
            column_length=column_length,
            column_nullable=column_nullable,
            column_precision=column_precision,
            column_scale=column_scale,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="format")
    def format(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "format", []))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80220eb995180beee0d1676df89ba274cb01fe3317a69ddad480b03ecdf65f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value)

    @builtins.property
    @jsii.member(jsii_name="columnType")
    def column_type(self) -> S3DataType:
        return typing.cast(S3DataType, jsii.get(self, "columnType"))

    @column_type.setter
    def column_type(self, value: S3DataType) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec75bcac759f4a03daec15189d5f05d7f62aeed8294e744c2451169110cf0ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnType", value)

    @builtins.property
    @jsii.member(jsii_name="columnDateFormat")
    def column_date_format(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnDateFormat"))

    @column_date_format.setter
    def column_date_format(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e8ce581e27ecc5edded0d05d4b39b73a461a6b5d8b50f74c0c09840af5dcf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnDateFormat", value)

    @builtins.property
    @jsii.member(jsii_name="columnIsPk")
    def column_is_pk(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "columnIsPk"))

    @column_is_pk.setter
    def column_is_pk(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d86165a8ba575b148eff7dd55e4a51de55c6d4a66e580e09a55431dcd18b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnIsPk", value)

    @builtins.property
    @jsii.member(jsii_name="columnLength")
    def column_length(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnLength"))

    @column_length.setter
    def column_length(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3b0f54ebb95bba95206c63f90edef25902e73c946ec0ccb60baf550379a8b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnLength", value)

    @builtins.property
    @jsii.member(jsii_name="columnNullable")
    def column_nullable(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "columnNullable"))

    @column_nullable.setter
    def column_nullable(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe876300e6bda54763aa88c26ae752fe8cf94994d8936aa8aaf2565df500565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnNullable", value)

    @builtins.property
    @jsii.member(jsii_name="columnPrecision")
    def column_precision(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnPrecision"))

    @column_precision.setter
    def column_precision(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ae40927c6a424b797a1f75f8f1533f59de272bb3a765cb413d1e2ece28e319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnPrecision", value)

    @builtins.property
    @jsii.member(jsii_name="columnScale")
    def column_scale(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnScale"))

    @column_scale.setter
    def column_scale(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a056f41e00441aa674c5b176226882ca7c027b91fd6bf757e31ee333c4cdc895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnScale", value)


@jsii.data_type(
    jsii_type="dms-patterns.TableColumnProps",
    jsii_struct_bases=[],
    name_mapping={
        "column_name": "columnName",
        "column_type": "columnType",
        "column_date_format": "columnDateFormat",
        "column_is_pk": "columnIsPk",
        "column_length": "columnLength",
        "column_nullable": "columnNullable",
        "column_precision": "columnPrecision",
        "column_scale": "columnScale",
    },
)
class TableColumnProps:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        column_type: S3DataType,
        column_date_format: typing.Optional[builtins.str] = None,
        column_is_pk: typing.Optional[builtins.bool] = None,
        column_length: typing.Optional[jsii.Number] = None,
        column_nullable: typing.Optional[builtins.bool] = None,
        column_precision: typing.Optional[jsii.Number] = None,
        column_scale: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column_name: 
        :param column_type: 
        :param column_date_format: 
        :param column_is_pk: 
        :param column_length: 
        :param column_nullable: 
        :param column_precision: 
        :param column_scale: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7243892de03508be88ced0959cf805d40f39502b1f5e3c96272fabc162e2a390)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument column_type", value=column_type, expected_type=type_hints["column_type"])
            check_type(argname="argument column_date_format", value=column_date_format, expected_type=type_hints["column_date_format"])
            check_type(argname="argument column_is_pk", value=column_is_pk, expected_type=type_hints["column_is_pk"])
            check_type(argname="argument column_length", value=column_length, expected_type=type_hints["column_length"])
            check_type(argname="argument column_nullable", value=column_nullable, expected_type=type_hints["column_nullable"])
            check_type(argname="argument column_precision", value=column_precision, expected_type=type_hints["column_precision"])
            check_type(argname="argument column_scale", value=column_scale, expected_type=type_hints["column_scale"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "column_type": column_type,
        }
        if column_date_format is not None:
            self._values["column_date_format"] = column_date_format
        if column_is_pk is not None:
            self._values["column_is_pk"] = column_is_pk
        if column_length is not None:
            self._values["column_length"] = column_length
        if column_nullable is not None:
            self._values["column_nullable"] = column_nullable
        if column_precision is not None:
            self._values["column_precision"] = column_precision
        if column_scale is not None:
            self._values["column_scale"] = column_scale

    @builtins.property
    def column_name(self) -> builtins.str:
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def column_type(self) -> S3DataType:
        result = self._values.get("column_type")
        assert result is not None, "Required property 'column_type' is missing"
        return typing.cast(S3DataType, result)

    @builtins.property
    def column_date_format(self) -> typing.Optional[builtins.str]:
        result = self._values.get("column_date_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def column_is_pk(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("column_is_pk")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def column_length(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("column_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def column_nullable(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("column_nullable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def column_precision(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("column_precision")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def column_scale(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("column_scale")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableColumnProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TableMappings(metaclass=jsii.JSIIMeta, jsii_type="dms-patterns.TableMappings"):
    def __init__(self, rules: typing.Optional[typing.Sequence[Rule]] = None) -> None:
        '''
        :param rules: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23f3c641834f2e1ef5f1c1c33ae6d90ca86d31d67d60177e66b94e155eaa390)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        jsii.create(self.__class__, self, [rules])

    @jsii.member(jsii_name="addRule")
    def add_rule(self, rule: Rule) -> None:
        '''
        :param rule: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e10cd2e09cc813555c07ffc2dee4c144fc9d6a8d2e3e57596fe4ab06675fc3)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(None, jsii.invoke(self, "addRule", [rule]))

    @jsii.member(jsii_name="format")
    def format(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "format", []))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "toJSON", []))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> typing.List[Rule]:
        return typing.cast(typing.List[Rule], jsii.get(self, "rules"))

    @rules.setter
    def rules(self, value: typing.List[Rule]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51f422c1db5f1c5f8f61a174baf218c74a1fd3ad17e98519a917a86cc05c7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rules", value)


@jsii.data_type(
    jsii_type="dms-patterns.TableProps",
    jsii_struct_bases=[],
    name_mapping={
        "table_columns": "tableColumns",
        "table_name": "tableName",
        "table_owner": "tableOwner",
        "table_path": "tablePath",
    },
)
class TableProps:
    def __init__(
        self,
        *,
        table_columns: typing.Sequence[TableColumn],
        table_name: builtins.str,
        table_owner: builtins.str,
        table_path: builtins.str,
    ) -> None:
        '''
        :param table_columns: 
        :param table_name: 
        :param table_owner: 
        :param table_path: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d90ec3b0e7cdf388ba48614a76bb49ecc32b5b0090c9d55a5cfa749c08441c)
            check_type(argname="argument table_columns", value=table_columns, expected_type=type_hints["table_columns"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument table_owner", value=table_owner, expected_type=type_hints["table_owner"])
            check_type(argname="argument table_path", value=table_path, expected_type=type_hints["table_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_columns": table_columns,
            "table_name": table_name,
            "table_owner": table_owner,
            "table_path": table_path,
        }

    @builtins.property
    def table_columns(self) -> typing.List[TableColumn]:
        result = self._values.get("table_columns")
        assert result is not None, "Required property 'table_columns' is missing"
        return typing.cast(typing.List[TableColumn], result)

    @builtins.property
    def table_name(self) -> builtins.str:
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_owner(self) -> builtins.str:
        result = self._values.get("table_owner")
        assert result is not None, "Required property 'table_owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_path(self) -> builtins.str:
        result = self._values.get("table_path")
        assert result is not None, "Required property 'table_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TableSettings(
    Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.TableSettings",
):
    def __init__(
        self,
        *,
        object_locator: typing.Union["TableSettingsObjectLocator", typing.Dict[builtins.str, typing.Any]],
        lob_settings: typing.Optional[typing.Union[LobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        parallel_load: typing.Optional[typing.Union[ParallelLoad, typing.Dict[builtins.str, typing.Any]]] = None,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        load_order: typing.Optional[jsii.Number] = None,
        rule_action: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_locator: 
        :param lob_settings: 
        :param parallel_load: 
        :param filters: 
        :param load_order: 
        :param rule_action: 
        :param rule_id: 
        :param rule_name: 
        '''
        props = TableSettingsProps(
            object_locator=object_locator,
            lob_settings=lob_settings,
            parallel_load=parallel_load,
            filters=filters,
            load_order=load_order,
            rule_action=rule_action,
            rule_id=rule_id,
            rule_name=rule_name,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="format")
    def format(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "format", []))

    @builtins.property
    @jsii.member(jsii_name="objectLocator")
    def object_locator(self) -> "TableSettingsObjectLocator":
        return typing.cast("TableSettingsObjectLocator", jsii.get(self, "objectLocator"))

    @object_locator.setter
    def object_locator(self, value: "TableSettingsObjectLocator") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ef9130a16d39e1876b72db647e52380244adfe272d9b233f5a78ba1a308ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectLocator", value)

    @builtins.property
    @jsii.member(jsii_name="ruleType")
    def rule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleType"))

    @rule_type.setter
    def rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e5eed2acba6f9af1e1b1dc3673abf25f235a21931c4bb04bde7ab3677ac252e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleType", value)

    @builtins.property
    @jsii.member(jsii_name="lobSettings")
    def lob_settings(self) -> typing.Optional[LobSettings]:
        return typing.cast(typing.Optional[LobSettings], jsii.get(self, "lobSettings"))

    @lob_settings.setter
    def lob_settings(self, value: typing.Optional[LobSettings]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e000ace3cd659a98cf262614673ff2c7a6d5b2c9a5b96bc40ef830ddd34d0a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lobSettings", value)

    @builtins.property
    @jsii.member(jsii_name="parallelLoad")
    def parallel_load(self) -> typing.Optional[ParallelLoad]:
        return typing.cast(typing.Optional[ParallelLoad], jsii.get(self, "parallelLoad"))

    @parallel_load.setter
    def parallel_load(self, value: typing.Optional[ParallelLoad]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57130f363855bdf10056bd5b0eb58b7558478b7e4f171146412c4a434bbb05ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelLoad", value)


@jsii.data_type(
    jsii_type="dms-patterns.TableSettingsObjectLocator",
    jsii_struct_bases=[ObjectLocator],
    name_mapping={"schema_name": "schemaName", "table_name": "tableName"},
)
class TableSettingsObjectLocator(ObjectLocator):
    def __init__(
        self,
        *,
        schema_name: builtins.str,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_name: 
        :param table_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b63e0d2f59d1d357d6bbbc715d0a8927b406fa2279b845d8e8a16f8ea3be0ead)
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema_name": schema_name,
        }
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def schema_name(self) -> builtins.str:
        result = self._values.get("schema_name")
        assert result is not None, "Required property 'schema_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableSettingsObjectLocator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="dms-patterns.TableSettingsProps",
    jsii_struct_bases=[RuleProps],
    name_mapping={
        "filters": "filters",
        "load_order": "loadOrder",
        "rule_action": "ruleAction",
        "rule_id": "ruleId",
        "rule_name": "ruleName",
        "object_locator": "objectLocator",
        "lob_settings": "lobSettings",
        "parallel_load": "parallelLoad",
    },
)
class TableSettingsProps(RuleProps):
    def __init__(
        self,
        *,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        load_order: typing.Optional[jsii.Number] = None,
        rule_action: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
        object_locator: typing.Union[TableSettingsObjectLocator, typing.Dict[builtins.str, typing.Any]],
        lob_settings: typing.Optional[typing.Union[LobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        parallel_load: typing.Optional[typing.Union[ParallelLoad, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param filters: 
        :param load_order: 
        :param rule_action: 
        :param rule_id: 
        :param rule_name: 
        :param object_locator: 
        :param lob_settings: 
        :param parallel_load: 
        '''
        if isinstance(object_locator, dict):
            object_locator = TableSettingsObjectLocator(**object_locator)
        if isinstance(lob_settings, dict):
            lob_settings = LobSettings(**lob_settings)
        if isinstance(parallel_load, dict):
            parallel_load = ParallelLoad(**parallel_load)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e1314e4536f4c45a4258d7b5a4e7779015d9a75e89ff5a6047948bdbbc6e08)
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument load_order", value=load_order, expected_type=type_hints["load_order"])
            check_type(argname="argument rule_action", value=rule_action, expected_type=type_hints["rule_action"])
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument object_locator", value=object_locator, expected_type=type_hints["object_locator"])
            check_type(argname="argument lob_settings", value=lob_settings, expected_type=type_hints["lob_settings"])
            check_type(argname="argument parallel_load", value=parallel_load, expected_type=type_hints["parallel_load"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_locator": object_locator,
        }
        if filters is not None:
            self._values["filters"] = filters
        if load_order is not None:
            self._values["load_order"] = load_order
        if rule_action is not None:
            self._values["rule_action"] = rule_action
        if rule_id is not None:
            self._values["rule_id"] = rule_id
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if lob_settings is not None:
            self._values["lob_settings"] = lob_settings
        if parallel_load is not None:
            self._values["parallel_load"] = parallel_load

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def load_order(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("load_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rule_action(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_locator(self) -> TableSettingsObjectLocator:
        result = self._values.get("object_locator")
        assert result is not None, "Required property 'object_locator' is missing"
        return typing.cast(TableSettingsObjectLocator, result)

    @builtins.property
    def lob_settings(self) -> typing.Optional[LobSettings]:
        result = self._values.get("lob_settings")
        return typing.cast(typing.Optional[LobSettings], result)

    @builtins.property
    def parallel_load(self) -> typing.Optional[ParallelLoad]:
        result = self._values.get("parallel_load")
        return typing.cast(typing.Optional[ParallelLoad], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableSettingsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskSettings(metaclass=jsii.JSIIMeta, jsii_type="dms-patterns.TaskSettings"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "toJSON", []))


@jsii.enum(jsii_type="dms-patterns.TransformationAction")
class TransformationAction(enum.Enum):
    ADD_COLUMN = "ADD_COLUMN"
    INCLUDE_COLUMN = "INCLUDE_COLUMN"
    REMOVE_COLUMN = "REMOVE_COLUMN"
    RENAME = "RENAME"
    CONVERT_LOWERCASE = "CONVERT_LOWERCASE"
    CONVERT_UPPERCASE = "CONVERT_UPPERCASE"
    ADD_PREFIX = "ADD_PREFIX"
    REMOVE_PREFIX = "REMOVE_PREFIX"
    REPLACE_PREFIX = "REPLACE_PREFIX"
    ADD_SUFFIX = "ADD_SUFFIX"
    REMOVE_SUFFIX = "REMOVE_SUFFIX"
    REPLACE_SUFFIX = "REPLACE_SUFFIX"
    DEFINE_PRIMARY_KEY = "DEFINE_PRIMARY_KEY"
    CHANGE_DATA_TYPE = "CHANGE_DATA_TYPE"
    ADD_BEFORE_IMAGE_COLUMNS = "ADD_BEFORE_IMAGE_COLUMNS"


@jsii.data_type(
    jsii_type="dms-patterns.TransformationObjectLocator",
    jsii_struct_bases=[ObjectLocator],
    name_mapping={
        "schema_name": "schemaName",
        "table_name": "tableName",
        "column_name": "columnName",
        "data_type": "dataType",
        "index_tablespace_name": "indexTablespaceName",
        "table_tablespace_name": "tableTablespaceName",
    },
)
class TransformationObjectLocator(ObjectLocator):
    def __init__(
        self,
        *,
        schema_name: builtins.str,
        table_name: typing.Optional[builtins.str] = None,
        column_name: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[typing.Union[DataTypeParams, typing.Dict[builtins.str, typing.Any]]] = None,
        index_tablespace_name: typing.Optional[builtins.str] = None,
        table_tablespace_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema_name: 
        :param table_name: 
        :param column_name: 
        :param data_type: 
        :param index_tablespace_name: 
        :param table_tablespace_name: 
        '''
        if isinstance(data_type, dict):
            data_type = DataTypeParams(**data_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d374daa2ad0ef0e8cf39807fc2d7f332dc8ed92a0704b6631b366728aa4e9a4)
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument index_tablespace_name", value=index_tablespace_name, expected_type=type_hints["index_tablespace_name"])
            check_type(argname="argument table_tablespace_name", value=table_tablespace_name, expected_type=type_hints["table_tablespace_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema_name": schema_name,
        }
        if table_name is not None:
            self._values["table_name"] = table_name
        if column_name is not None:
            self._values["column_name"] = column_name
        if data_type is not None:
            self._values["data_type"] = data_type
        if index_tablespace_name is not None:
            self._values["index_tablespace_name"] = index_tablespace_name
        if table_tablespace_name is not None:
            self._values["table_tablespace_name"] = table_tablespace_name

    @builtins.property
    def schema_name(self) -> builtins.str:
        result = self._values.get("schema_name")
        assert result is not None, "Required property 'schema_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def column_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("column_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[DataTypeParams]:
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[DataTypeParams], result)

    @builtins.property
    def index_tablespace_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("index_tablespace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_tablespace_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_tablespace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransformationObjectLocator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransformationRule(
    Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.TransformationRule",
):
    def __init__(
        self,
        *,
        object_locator: typing.Union[TransformationObjectLocator, typing.Dict[builtins.str, typing.Any]],
        rule_target: "TransformationTarget",
        before_image_def: typing.Optional[typing.Union[BeforeImageDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
        data_type: typing.Optional[typing.Union[DataTypeParams, typing.Dict[builtins.str, typing.Any]]] = None,
        expression: typing.Optional[builtins.str] = None,
        old_value: typing.Optional[builtins.str] = None,
        primary_key_def: typing.Optional[typing.Union[PrimaryKeyDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
        value: typing.Optional[builtins.str] = None,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        load_order: typing.Optional[jsii.Number] = None,
        rule_action: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_locator: 
        :param rule_target: 
        :param before_image_def: 
        :param data_type: 
        :param expression: 
        :param old_value: 
        :param primary_key_def: 
        :param value: 
        :param filters: 
        :param load_order: 
        :param rule_action: 
        :param rule_id: 
        :param rule_name: 
        '''
        props = TransformationRuleProps(
            object_locator=object_locator,
            rule_target=rule_target,
            before_image_def=before_image_def,
            data_type=data_type,
            expression=expression,
            old_value=old_value,
            primary_key_def=primary_key_def,
            value=value,
            filters=filters,
            load_order=load_order,
            rule_action=rule_action,
            rule_id=rule_id,
            rule_name=rule_name,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="format")
    def format(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "format", []))

    @builtins.property
    @jsii.member(jsii_name="objectLocator")
    def object_locator(self) -> TransformationObjectLocator:
        return typing.cast(TransformationObjectLocator, jsii.get(self, "objectLocator"))

    @object_locator.setter
    def object_locator(self, value: TransformationObjectLocator) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f7949e5d8b2f7f03eea9426381cc4e0c49929d89ab0b24accc91564f1c38d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectLocator", value)

    @builtins.property
    @jsii.member(jsii_name="ruleTarget")
    def rule_target(self) -> "TransformationTarget":
        return typing.cast("TransformationTarget", jsii.get(self, "ruleTarget"))

    @rule_target.setter
    def rule_target(self, value: "TransformationTarget") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7566816d326f0a6fb488428cce7d8a80ac8c1038f049b223f336779a63fd15e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleTarget", value)

    @builtins.property
    @jsii.member(jsii_name="ruleType")
    def rule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleType"))

    @rule_type.setter
    def rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140e338e0c357596e6989b27b1ef655a49909c73558b9ea35122427f6b96cfcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleType", value)

    @builtins.property
    @jsii.member(jsii_name="beforeImageDef")
    def before_image_def(self) -> typing.Optional[BeforeImageDefinition]:
        return typing.cast(typing.Optional[BeforeImageDefinition], jsii.get(self, "beforeImageDef"))

    @before_image_def.setter
    def before_image_def(self, value: typing.Optional[BeforeImageDefinition]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__835106ba3ee1a6cb22464ded9fddd87430b5fc345c7610a9c0618ca5e03bd03f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "beforeImageDef", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> typing.Optional[DataTypeParams]:
        return typing.cast(typing.Optional[DataTypeParams], jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: typing.Optional[DataTypeParams]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d627dfd662163956e4d59f8be63c4edf2cb3f1bea1eb31a6de936db98019c3a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f8edc0ac5c5b2f0c1446e4dd3a80328983a379757510309b1a9c1a14707931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value)

    @builtins.property
    @jsii.member(jsii_name="oldValue")
    def old_value(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oldValue"))

    @old_value.setter
    def old_value(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a6ac918e1907fd47a4069856a7c03722ddf33b7da686297d13de0c078b7ddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oldValue", value)

    @builtins.property
    @jsii.member(jsii_name="primaryKeyDef")
    def primary_key_def(self) -> typing.Optional[PrimaryKeyDefinition]:
        return typing.cast(typing.Optional[PrimaryKeyDefinition], jsii.get(self, "primaryKeyDef"))

    @primary_key_def.setter
    def primary_key_def(self, value: typing.Optional[PrimaryKeyDefinition]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797d01d424b51c5a98089474804335f6823c2feea31f349717b24252c96c9faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKeyDef", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "value"))

    @value.setter
    def value(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab5ec05a6fe144f820de18a0a711c6ded935b7c03919c9fbd022b976f839c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)


@jsii.data_type(
    jsii_type="dms-patterns.TransformationRuleProps",
    jsii_struct_bases=[RuleProps],
    name_mapping={
        "filters": "filters",
        "load_order": "loadOrder",
        "rule_action": "ruleAction",
        "rule_id": "ruleId",
        "rule_name": "ruleName",
        "object_locator": "objectLocator",
        "rule_target": "ruleTarget",
        "before_image_def": "beforeImageDef",
        "data_type": "dataType",
        "expression": "expression",
        "old_value": "oldValue",
        "primary_key_def": "primaryKeyDef",
        "value": "value",
    },
)
class TransformationRuleProps(RuleProps):
    def __init__(
        self,
        *,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        load_order: typing.Optional[jsii.Number] = None,
        rule_action: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
        object_locator: typing.Union[TransformationObjectLocator, typing.Dict[builtins.str, typing.Any]],
        rule_target: "TransformationTarget",
        before_image_def: typing.Optional[typing.Union[BeforeImageDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
        data_type: typing.Optional[typing.Union[DataTypeParams, typing.Dict[builtins.str, typing.Any]]] = None,
        expression: typing.Optional[builtins.str] = None,
        old_value: typing.Optional[builtins.str] = None,
        primary_key_def: typing.Optional[typing.Union[PrimaryKeyDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filters: 
        :param load_order: 
        :param rule_action: 
        :param rule_id: 
        :param rule_name: 
        :param object_locator: 
        :param rule_target: 
        :param before_image_def: 
        :param data_type: 
        :param expression: 
        :param old_value: 
        :param primary_key_def: 
        :param value: 
        '''
        if isinstance(object_locator, dict):
            object_locator = TransformationObjectLocator(**object_locator)
        if isinstance(before_image_def, dict):
            before_image_def = BeforeImageDefinition(**before_image_def)
        if isinstance(data_type, dict):
            data_type = DataTypeParams(**data_type)
        if isinstance(primary_key_def, dict):
            primary_key_def = PrimaryKeyDefinition(**primary_key_def)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c9ec272f66fca4d7222446f6b2fa9a47f425c2b226eea377595b32d2428889)
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument load_order", value=load_order, expected_type=type_hints["load_order"])
            check_type(argname="argument rule_action", value=rule_action, expected_type=type_hints["rule_action"])
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument object_locator", value=object_locator, expected_type=type_hints["object_locator"])
            check_type(argname="argument rule_target", value=rule_target, expected_type=type_hints["rule_target"])
            check_type(argname="argument before_image_def", value=before_image_def, expected_type=type_hints["before_image_def"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument old_value", value=old_value, expected_type=type_hints["old_value"])
            check_type(argname="argument primary_key_def", value=primary_key_def, expected_type=type_hints["primary_key_def"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_locator": object_locator,
            "rule_target": rule_target,
        }
        if filters is not None:
            self._values["filters"] = filters
        if load_order is not None:
            self._values["load_order"] = load_order
        if rule_action is not None:
            self._values["rule_action"] = rule_action
        if rule_id is not None:
            self._values["rule_id"] = rule_id
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if before_image_def is not None:
            self._values["before_image_def"] = before_image_def
        if data_type is not None:
            self._values["data_type"] = data_type
        if expression is not None:
            self._values["expression"] = expression
        if old_value is not None:
            self._values["old_value"] = old_value
        if primary_key_def is not None:
            self._values["primary_key_def"] = primary_key_def
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def load_order(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("load_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rule_action(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_locator(self) -> TransformationObjectLocator:
        result = self._values.get("object_locator")
        assert result is not None, "Required property 'object_locator' is missing"
        return typing.cast(TransformationObjectLocator, result)

    @builtins.property
    def rule_target(self) -> "TransformationTarget":
        result = self._values.get("rule_target")
        assert result is not None, "Required property 'rule_target' is missing"
        return typing.cast("TransformationTarget", result)

    @builtins.property
    def before_image_def(self) -> typing.Optional[BeforeImageDefinition]:
        result = self._values.get("before_image_def")
        return typing.cast(typing.Optional[BeforeImageDefinition], result)

    @builtins.property
    def data_type(self) -> typing.Optional[DataTypeParams]:
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[DataTypeParams], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def old_value(self) -> typing.Optional[builtins.str]:
        result = self._values.get("old_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_key_def(self) -> typing.Optional[PrimaryKeyDefinition]:
        result = self._values.get("primary_key_def")
        return typing.cast(typing.Optional[PrimaryKeyDefinition], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransformationRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="dms-patterns.TransformationTarget")
class TransformationTarget(enum.Enum):
    SCHEMA = "SCHEMA"
    TABLE = "TABLE"
    COLUMN = "COLUMN"
    TABLE_TABLESPACE = "TABLE_TABLESPACE"
    INDEX_TABLESPACE = "INDEX_TABLESPACE"


__all__ = [
    "BeforeImageDefinition",
    "CapacityUnits",
    "DataTypeParams",
    "DmsVpcRoleStack",
    "EndpointEngine",
    "EndpointType",
    "LobSettings",
    "MySql2S3",
    "MySql2S3Props",
    "MySqlEndpoint",
    "MySqlProps",
    "MySqlSettings",
    "ObjectLocator",
    "ParallelLoad",
    "PostgreSQLEndpoint",
    "PostgreSqlSettings",
    "Postgres2S3",
    "Postgres2S3Props",
    "PostgresProps",
    "PrimaryKeyDefinition",
    "ReplicationTypes",
    "Rule",
    "RuleProps",
    "RuleType",
    "S32s3",
    "S32s3Props",
    "S3DataType",
    "S3EndpointBase",
    "S3EndpointBaseProps",
    "S3Schema",
    "S3SourceEndpoint",
    "S3SourceEndpointProps",
    "S3SourceEndpointSettings",
    "S3TargetEndpoint",
    "S3TargetEndpointProps",
    "S3TargetEndpointSettings",
    "SelectionAction",
    "SelectionObjectLocator",
    "SelectionRule",
    "SelectionRuleProps",
    "Table",
    "TableColumn",
    "TableColumnProps",
    "TableMappings",
    "TableProps",
    "TableSettings",
    "TableSettingsObjectLocator",
    "TableSettingsProps",
    "TaskSettings",
    "TransformationAction",
    "TransformationObjectLocator",
    "TransformationRule",
    "TransformationRuleProps",
    "TransformationTarget",
]

publication.publish()

def _typecheckingstub__667f9af382cf67ab293493b3b38f65d34278a9e7e71ad6c5fba49f97db7ef0b6(
    *,
    column_filter: builtins.str,
    column_prefix: typing.Optional[builtins.str] = None,
    column_suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6f116624ae75de090d0dab02f53e269fe7c4be4f68398384c2bfa3c52f6d76(
    *,
    type: builtins.str,
    length: typing.Optional[jsii.Number] = None,
    precision: typing.Optional[jsii.Number] = None,
    scale: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843b532d6facd990ffa3b6ad249a450c491be54c02decf0dc747700aca51be67(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    stack_name: typing.Optional[builtins.str] = None,
    suppress_template_indentation: typing.Optional[builtins.bool] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7995548b12ccb95d7a5ad71d3d8059e9076888b80bb0e5e7d3490bcc273dcfe(
    value: _aws_cdk_aws_iam_ceddda9d.Role,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e355e58daa23240631040b055b0690209970951f9f0a085aecc9d71008e46b(
    value: _aws_cdk_aws_iam_ceddda9d.Role,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f362a317b2a4c48d9f96f4e8ddfa202006971bfa58d85a7bc2ea35027b7da971(
    *,
    bulk_max_size: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8421fc107c5b30d6b1bba405e4c64f86fca88bfcf1b114f95182c5828f3af5c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_arn: builtins.str,
    database_name: builtins.str,
    my_sql_endpoint_settings: typing.Union[MySqlSettings, typing.Dict[builtins.str, typing.Any]],
    replication_config_identifier: builtins.str,
    table_mappings: TableMappings,
    compute_config: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    replication_settings: typing.Any = None,
    s3target_endpoint_settings: typing.Optional[typing.Union[S3TargetEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    task_settings: typing.Optional[TaskSettings] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c02ae8d7d9825f132aa35849afcd7bcf5d204374923a3ecf283b00354e93d5f(
    value: MySqlEndpoint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c006d4a0822f1edc4d418bbbbb0fe55cec899bbb79b77fe3be3d564414a9a765(
    value: S3TargetEndpoint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a38656d8900cd716870b31d5f1dad68ff4a4f4204729f0b7335fa160d5fe00e(
    *,
    bucket_arn: builtins.str,
    database_name: builtins.str,
    my_sql_endpoint_settings: typing.Union[MySqlSettings, typing.Dict[builtins.str, typing.Any]],
    replication_config_identifier: builtins.str,
    table_mappings: TableMappings,
    compute_config: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    replication_settings: typing.Any = None,
    s3target_endpoint_settings: typing.Optional[typing.Union[S3TargetEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    task_settings: typing.Optional[TaskSettings] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5bc95e368ec4b22334846ac3f52325fe466b8b61f0343e121ca0b76b643ecb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    database_name: builtins.str,
    endpoint_identifier: builtins.str,
    endpoint_type: builtins.str,
    my_sql_endpoint_settings: typing.Union[MySqlSettings, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ec09267c8ea6591e86ffd1305748c424caece1f84f49a7d8997080bf89ac75(
    *,
    database_name: builtins.str,
    endpoint_identifier: builtins.str,
    endpoint_type: builtins.str,
    my_sql_endpoint_settings: typing.Union[MySqlSettings, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5b4fcc2c06c6dddd07db0353bf6c0ab65f4be51ff6ff209848fd89f5f14b83(
    *,
    secrets_manager_secret_id: builtins.str,
    after_connect_script: typing.Optional[builtins.str] = None,
    clean_source_metadata_on_mismatch: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    events_poll_interval: typing.Optional[jsii.Number] = None,
    server_timezone: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdca11b6edf0314b444ecefb2470310061565728c95917175376d6f74f579909(
    *,
    schema_name: builtins.str,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b04864cd73a655bdf0e25b5109c21dc8d7fb684d34856b872bd9f499292d13(
    *,
    type: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    boundaries: typing.Optional[typing.Sequence[typing.Sequence[typing.Any]]] = None,
    collection_count_from_metadata: typing.Optional[builtins.bool] = None,
    columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_records_skip_per_page: typing.Optional[jsii.Number] = None,
    number_of_partitions: typing.Optional[jsii.Number] = None,
    partitions: typing.Optional[typing.Sequence[builtins.str]] = None,
    subpartitions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92befc2f4d59e8aa32ef5975d2f8b4d31cb75cf228b27e2b58db90819db62d16(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    database_name: builtins.str,
    endpoint_identifier: builtins.str,
    endpoint_type: builtins.str,
    postgres_endpoint_settings: typing.Union[PostgreSqlSettings, typing.Dict[builtins.str, typing.Any]],
    port: typing.Optional[jsii.Number] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825a166842d541be750f985e572e19c7fd47bb992e3fe9cf458d391be4d579a1(
    *,
    secrets_manager_secret_id: builtins.str,
    capture_ddls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ddl_artifacts_schema: typing.Optional[builtins.str] = None,
    execute_timeout: typing.Optional[jsii.Number] = None,
    fail_tasks_on_lob_truncation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    heartbeat_frequency: typing.Optional[jsii.Number] = None,
    heartbeat_schema: typing.Optional[builtins.str] = None,
    map_boolean_as_boolean: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    slot_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b7eb97a04f77db1abbb83e5bef8f0f8b611eda71d81076a7dc2c49ae8f8b11(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_arn: builtins.str,
    database_name: builtins.str,
    postgres_endpoint_settings: typing.Union[PostgreSqlSettings, typing.Dict[builtins.str, typing.Any]],
    replication_config_identifier: builtins.str,
    table_mappings: TableMappings,
    compute_config: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    replication_settings: typing.Any = None,
    s3target_endpoint_settings: typing.Optional[typing.Union[S3TargetEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    task_settings: typing.Optional[TaskSettings] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a7364f6600a9916d4829e7729eb494622007b2a7ea54da1e5fd8429ee28aca(
    value: PostgreSQLEndpoint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a1fabb06c784c92505891c1da8270dbe1db8cb220fc612efff2947078e9c16(
    value: S3TargetEndpoint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15f1eedac7dd2787fe56212e68f33d80c6a0f8dbd41c047f80f4be82ec402aa(
    *,
    bucket_arn: builtins.str,
    database_name: builtins.str,
    postgres_endpoint_settings: typing.Union[PostgreSqlSettings, typing.Dict[builtins.str, typing.Any]],
    replication_config_identifier: builtins.str,
    table_mappings: TableMappings,
    compute_config: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnReplicationConfig.ComputeConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    replication_settings: typing.Any = None,
    s3target_endpoint_settings: typing.Optional[typing.Union[S3TargetEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    task_settings: typing.Optional[TaskSettings] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cddd0113a73e09bfde59d3dda86fce808a8794864fd048933a6718c3909dcf22(
    *,
    database_name: builtins.str,
    endpoint_identifier: builtins.str,
    endpoint_type: builtins.str,
    postgres_endpoint_settings: typing.Union[PostgreSqlSettings, typing.Dict[builtins.str, typing.Any]],
    port: typing.Optional[jsii.Number] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1911bb297fa0811b0ce4984bb2a990c557520cc0ff87f3b86640baa9b78f01d(
    *,
    columns: typing.Sequence[builtins.str],
    name: builtins.str,
    origin: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207c6b48859ea1f50c9bbf11f2566d2b9923b91096f964cd2079d68a964b8f5a(
    value: typing.Optional[typing.List[typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20724d4988391d538c8aa6181ac4d06a714127dd37dea8649aecaec36b4b6f12(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9598e29308a5c2081484b2d38a2094166354a77d50704c28c79ea8469266e22b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491f151bc24f8115e16e3ead727c88d5a24646dc4d12d70943bb9be46650030c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a420fb93fe547b3b5967fee97e927e6d6bf41d1130ce8d5d7958398248f5b239(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a07a66781a531a483c4386a36184797fdee7e20defd89bc8ea157ece01b747(
    *,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    load_order: typing.Optional[jsii.Number] = None,
    rule_action: typing.Optional[builtins.str] = None,
    rule_id: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec25ea4b2542a04f088a34d74d7319dcd90a8a2065924b9ab647e3424bf5fc5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    source_bucket_arn: builtins.str,
    table_mappings: TableMappings,
    target_bucket_arn: builtins.str,
    source_endpoint_settings: typing.Optional[typing.Union[S3SourceEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    target_endpoint_settings: typing.Optional[typing.Union[S3TargetEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    task_settings: typing.Optional[TaskSettings] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c2abb42f459f87f75dbca212cf2761cefa8ab9d1913893f3d46555875c3f63(
    value: _aws_cdk_aws_dms_ceddda9d.CfnReplicationTask,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d810c3375d81a6d1d1e310f6ee59588499bd26ce5a9857f7a4c53cc3c278a9c(
    value: S3SourceEndpoint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa4d6f2a789fbb7cb1543e06bf9c9316b1ad59934465a201ff520c50cf0bece(
    value: S3TargetEndpoint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c83763074671fe62265290ad2260669fa2bc0bd70453d0a4fa2c6049f083c6(
    *,
    source_bucket_arn: builtins.str,
    table_mappings: TableMappings,
    target_bucket_arn: builtins.str,
    source_endpoint_settings: typing.Optional[typing.Union[S3SourceEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    target_endpoint_settings: typing.Optional[typing.Union[S3TargetEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    task_settings: typing.Optional[TaskSettings] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cda125a2b8cad1fba43f8dfe14a0d6aad849dde17f4ef8251b166ee410d4284(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_arn: builtins.str,
    endpoint_type: builtins.str,
    s3_settings: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnEndpoint.S3SettingsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae81c7a64e63f164c8dbdd9d5047c60d6fab0e86881186fe0f07199a06a1f6fe(
    *,
    bucket_arn: builtins.str,
    endpoint_type: builtins.str,
    s3_settings: typing.Optional[typing.Union[_aws_cdk_aws_dms_ceddda9d.CfnEndpoint.S3SettingsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e2430c2582bb2398d9d9a4e39ba076488d3b00379fa9636259d8e12085decf(
    tables: typing.Optional[typing.Sequence[Table]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0903cba4fa3dad8d7553474e3581f8d27ab8cb2d2db82293e6fbd64ea82091f5(
    table: Table,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b526c8296db82e3b88e882a0e5c1e94ca144dccde76791364351d996361737be(
    value: typing.List[Table],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f708c7afa5634d65010d037fffae9e36e9151974b7816d3b18e000aa09356f6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_arn: builtins.str,
    s3_source_endpoint_settings: typing.Optional[typing.Union[S3SourceEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae62b5d8f0195172abe7f4ff82655f7badf90962ac262914ed9736ed869f9e73(
    *,
    bucket_arn: builtins.str,
    s3_source_endpoint_settings: typing.Optional[typing.Union[S3SourceEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5472049b0881129ac75caae713086dd7faba23e150cfa7ee846b666dfc605290(
    *,
    bucket_folder: typing.Optional[builtins.str] = None,
    cdc_path: typing.Optional[builtins.str] = None,
    csv_delimiter: typing.Optional[builtins.str] = None,
    csv_null_value: typing.Optional[builtins.str] = None,
    csv_row_delimiter: typing.Optional[builtins.str] = None,
    ignore_header_rows: typing.Optional[jsii.Number] = None,
    rfc4180: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444f504d5c7972ffde6e06307b69024cac924937bfc14a502cfae3dea1b853e3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_arn: builtins.str,
    s3_target_endpoint_settings: typing.Optional[typing.Union[S3TargetEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a63d7889b615ad96536c4a307322f56a1d10c7105e3da1fd4ebd973e23ecc3(
    *,
    bucket_arn: builtins.str,
    s3_target_endpoint_settings: typing.Optional[typing.Union[S3TargetEndpointSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13aa07b3157ed245b02c419e68a9056b33fd7059a8975452dcb4b768e0417a6(
    *,
    add_column_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    bucket_folder: typing.Optional[builtins.str] = None,
    canned_acl_for_objects: typing.Optional[builtins.str] = None,
    cdc_inserts_and_updates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cdc_inserts_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cdc_max_batch_interval: typing.Optional[jsii.Number] = None,
    cdc_min_file_size: typing.Optional[jsii.Number] = None,
    cdc_path: typing.Optional[builtins.str] = None,
    compression_type: typing.Optional[builtins.str] = None,
    csv_delimiter: typing.Optional[builtins.str] = None,
    csv_null_value: typing.Optional[builtins.str] = None,
    csv_row_delimiter: typing.Optional[builtins.str] = None,
    data_format: typing.Optional[builtins.str] = None,
    data_page_size: typing.Optional[jsii.Number] = None,
    dict_page_size_limit: typing.Optional[jsii.Number] = None,
    enable_statistics: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encoding_type: typing.Optional[builtins.str] = None,
    encryption_mode: typing.Optional[builtins.str] = None,
    include_op_for_full_load: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    parquet_timestamp_in_millisecond: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    parquet_version: typing.Optional[builtins.str] = None,
    preserve_transactions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    rfc4180: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    row_group_length: typing.Optional[jsii.Number] = None,
    server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    timestamp_column_name: typing.Optional[builtins.str] = None,
    use_task_start_time_for_full_load_timestamp: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ea00ab8131194666102cb41f06317a4eae504ec9438de5b78509f1d9a02b9d(
    *,
    schema_name: builtins.str,
    table_name: typing.Optional[builtins.str] = None,
    table_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b10ee67f01cd5b29d311598ec587c0f59ddbc66499745b9032abb8c35d115e(
    value: SelectionObjectLocator,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c03d3c6f0e2d06c6c46b2b375e6148d0b4c2ed1f2ee5c71017500e5e9811a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e930f6f98ef8924df1fd35c2dad91a1eb8aebf230ef829e26a85b641af217ead(
    value: typing.Optional[typing.List[typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b817073504973077b206c43b1254f2161c4774b5eddb65ec8a031c2de3674ddc(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7224a7df496e4ec105599c7b7ea2a2dfc92554bf69f5f9b690b599c7e1cbd3(
    *,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    load_order: typing.Optional[jsii.Number] = None,
    rule_action: typing.Optional[builtins.str] = None,
    rule_id: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    object_locator: typing.Union[SelectionObjectLocator, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5880519a9b236d385ff5105ca351a9d728d4c60c44b17f1b2375ed313bcd5deb(
    value: typing.List[TableColumn],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9350ff38a946b7c1c9cc58e210806a96a1598c2546fb4e41e75cc477ba84afcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04225f5d3257db1c0e410713e3c71b79525bcf331f8af533d65e7ef0b3f20f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10182c6f41621b1ebdb03e47a49272785affdbb4e191ef96afc37087f5f01a61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80220eb995180beee0d1676df89ba274cb01fe3317a69ddad480b03ecdf65f0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec75bcac759f4a03daec15189d5f05d7f62aeed8294e744c2451169110cf0ec(
    value: S3DataType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e8ce581e27ecc5edded0d05d4b39b73a461a6b5d8b50f74c0c09840af5dcf9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d86165a8ba575b148eff7dd55e4a51de55c6d4a66e580e09a55431dcd18b5c(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3b0f54ebb95bba95206c63f90edef25902e73c946ec0ccb60baf550379a8b3(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe876300e6bda54763aa88c26ae752fe8cf94994d8936aa8aaf2565df500565(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ae40927c6a424b797a1f75f8f1533f59de272bb3a765cb413d1e2ece28e319(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a056f41e00441aa674c5b176226882ca7c027b91fd6bf757e31ee333c4cdc895(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7243892de03508be88ced0959cf805d40f39502b1f5e3c96272fabc162e2a390(
    *,
    column_name: builtins.str,
    column_type: S3DataType,
    column_date_format: typing.Optional[builtins.str] = None,
    column_is_pk: typing.Optional[builtins.bool] = None,
    column_length: typing.Optional[jsii.Number] = None,
    column_nullable: typing.Optional[builtins.bool] = None,
    column_precision: typing.Optional[jsii.Number] = None,
    column_scale: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23f3c641834f2e1ef5f1c1c33ae6d90ca86d31d67d60177e66b94e155eaa390(
    rules: typing.Optional[typing.Sequence[Rule]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e10cd2e09cc813555c07ffc2dee4c144fc9d6a8d2e3e57596fe4ab06675fc3(
    rule: Rule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51f422c1db5f1c5f8f61a174baf218c74a1fd3ad17e98519a917a86cc05c7bf(
    value: typing.List[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d90ec3b0e7cdf388ba48614a76bb49ecc32b5b0090c9d55a5cfa749c08441c(
    *,
    table_columns: typing.Sequence[TableColumn],
    table_name: builtins.str,
    table_owner: builtins.str,
    table_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ef9130a16d39e1876b72db647e52380244adfe272d9b233f5a78ba1a308ed0(
    value: TableSettingsObjectLocator,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5eed2acba6f9af1e1b1dc3673abf25f235a21931c4bb04bde7ab3677ac252e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e000ace3cd659a98cf262614673ff2c7a6d5b2c9a5b96bc40ef830ddd34d0a49(
    value: typing.Optional[LobSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57130f363855bdf10056bd5b0eb58b7558478b7e4f171146412c4a434bbb05ad(
    value: typing.Optional[ParallelLoad],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63e0d2f59d1d357d6bbbc715d0a8927b406fa2279b845d8e8a16f8ea3be0ead(
    *,
    schema_name: builtins.str,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e1314e4536f4c45a4258d7b5a4e7779015d9a75e89ff5a6047948bdbbc6e08(
    *,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    load_order: typing.Optional[jsii.Number] = None,
    rule_action: typing.Optional[builtins.str] = None,
    rule_id: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    object_locator: typing.Union[TableSettingsObjectLocator, typing.Dict[builtins.str, typing.Any]],
    lob_settings: typing.Optional[typing.Union[LobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    parallel_load: typing.Optional[typing.Union[ParallelLoad, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d374daa2ad0ef0e8cf39807fc2d7f332dc8ed92a0704b6631b366728aa4e9a4(
    *,
    schema_name: builtins.str,
    table_name: typing.Optional[builtins.str] = None,
    column_name: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[typing.Union[DataTypeParams, typing.Dict[builtins.str, typing.Any]]] = None,
    index_tablespace_name: typing.Optional[builtins.str] = None,
    table_tablespace_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f7949e5d8b2f7f03eea9426381cc4e0c49929d89ab0b24accc91564f1c38d5(
    value: TransformationObjectLocator,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7566816d326f0a6fb488428cce7d8a80ac8c1038f049b223f336779a63fd15e2(
    value: TransformationTarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140e338e0c357596e6989b27b1ef655a49909c73558b9ea35122427f6b96cfcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835106ba3ee1a6cb22464ded9fddd87430b5fc345c7610a9c0618ca5e03bd03f(
    value: typing.Optional[BeforeImageDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d627dfd662163956e4d59f8be63c4edf2cb3f1bea1eb31a6de936db98019c3a0(
    value: typing.Optional[DataTypeParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f8edc0ac5c5b2f0c1446e4dd3a80328983a379757510309b1a9c1a14707931(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a6ac918e1907fd47a4069856a7c03722ddf33b7da686297d13de0c078b7ddb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797d01d424b51c5a98089474804335f6823c2feea31f349717b24252c96c9faa(
    value: typing.Optional[PrimaryKeyDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab5ec05a6fe144f820de18a0a711c6ded935b7c03919c9fbd022b976f839c99(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c9ec272f66fca4d7222446f6b2fa9a47f425c2b226eea377595b32d2428889(
    *,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    load_order: typing.Optional[jsii.Number] = None,
    rule_action: typing.Optional[builtins.str] = None,
    rule_id: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    object_locator: typing.Union[TransformationObjectLocator, typing.Dict[builtins.str, typing.Any]],
    rule_target: TransformationTarget,
    before_image_def: typing.Optional[typing.Union[BeforeImageDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
    data_type: typing.Optional[typing.Union[DataTypeParams, typing.Dict[builtins.str, typing.Any]]] = None,
    expression: typing.Optional[builtins.str] = None,
    old_value: typing.Optional[builtins.str] = None,
    primary_key_def: typing.Optional[typing.Union[PrimaryKeyDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
