'''
# aws-constructs-factories module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_constructs_factories`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-constructs-factories`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.constructsfactories`|

## Overview

This AWS Solutions Construct exposes the same code used to create our underlying resources as factories, so clients can create individual resources that are well-architected.
There are factories to create:

[Amazon S3 buckets](https://docs.aws.amazon.com/solutions/latest/constructs/aws-constructs-factories.html#s3-buckets) - Create a well architected S3 bucket (e.g. - includes an access logging bucket)
[AWS Step Functions state machines](https://docs.aws.amazon.com/solutions/latest/constructs/aws-constructs-factories.html#step-functions-state-machines) - Create a well architected Step Functions state machine and log group (e.g. log group has /aws/vendedlogs/ name prefix to avoid resource policy issues)

## S3 Buckets

Create fully well-architected S3 buckets with as little as one function call. Here is a minimal deployable pattern definition:

Typescript

```python
import { Construct } from 'constructs';
import { Stack, StackProps } from 'aws-cdk-lib';
import { ConstructsFactories } from '@aws-solutions-constructs/aws-constructs-factories';

const factories = new ConstructsFactories(this, 'MyFactories');

factories.s3BucketFactory('GoodBucket', {});
```

Python

```python
from aws_cdk import (
    Stack,
)
from constructs import Construct

from aws_solutions_constructs import (
    aws_constructs_factories as cf
)

factories = cf.ConstructsFactories(self, 'MyFactories')
factories.s3_bucket_factory('GoodBucket')
```

Java

```java
import software.constructs.Construct;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awsconstructs.services.constructsfactories.ConstructsFactories;
import software.amazon.awsconstructs.services.constructsfactories.S3BucketFactoryProps;

final ConstructsFactories factories = new ConstructsFactories(this, "MyFactories");
factories.s3BucketFactory("GoodBucket",
  new S3BucketFactoryProps.Builder().build());
```

# S3BucketFactory Function Signature

```python
s3BucketFactory(id: string, props: S3BucketFactoryProps): S3BucketFactoryResponse
```

# S3BucketFactoryProps

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|bucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.BucketProps.html)|Optional user provided props to override the default props for the S3 Bucket.|
|logS3AccessLogs?|`boolean`|Whether to turn on Access Logging for the S3 bucket. Creates an S3 bucket with associated storage costs for the logs. Enabling Access Logging is a best practice. default - true|
|loggingBucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.BucketProps.html)|Optional user provided props to override the default props for the S3 Logging Bucket.|

# S3BucketFactoryResponse

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|s3Bucket|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.Bucket.html)|The s3.Bucket created by the factory. |
|s3LoggingBucket?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.Bucket.html)|The s3.Bucket created by the construct as the logging bucket for the primary bucket. If the logS3AccessLogs property is false, this value will be undefined.|

# Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

* An S3 Content Bucket

  * AWS managed Server Side Encryption (AES256)
  * Lifecycle rule to transition objects to Glacier storage class in 90 days
  * Access Logging enabled
  * All Public access blocked
  * Versioning enabled
  * UpdateReplacePolicy is delete
  * Deletion policy is delete
  * Bucket policy requiring SecureTransport
* An S3 Bucket for Access Logs

  * AWS managed Server Side Encryption (AES256)
  * All public access blocked
  * Versioning enabled
  * UpdateReplacePolicy is delete
  * Deletion policy is delete
  * Bucket policy requiring SecureTransport
  * Bucket policy granting PutObject privileges to the S3 logging service, from the content bucket in the content bucket account.
  * cfn_nag suppression of access logging finding (not logging access to the access log bucket)

# Architecture

![Architecture Diagram](architecture.png)

## Step Functions State Machines

Create fully well-architected Step Functions state machine with log group. The log group name includes the vendedlogs prefix. Here
but is unique to the stack, avoiding naming collions between instances. is a minimal deployable pattern definition:

Typescript

```python
import { App, Stack } from "aws-cdk-lib";
import { ConstructsFactories } from "../../lib";
import { generateIntegStackName, CreateTestStateMachineDefinitionBody } from '@aws-solutions-constructs/core';
import { IntegTest } from '@aws-cdk/integ-tests-alpha';

const placeholderTask = new sftasks.EvaluateExpression(this, 'placeholder', {
  expression: '$.argOne + $.argTwo'
});

const factories = new ConstructsFactories(this, 'minimalImplementation');

factories.stateMachineFactory('testsm', {
  stateMachineProps: {
    definitionBody: sfn.DefinitionBody.fromChainable(placeholderTask)
  }
});
```

Python

```python

# Pending

```

Java

```java

// Pending

```

# stateMachineFactory Function Signature

```python
stateMachineFactory(id: string, props: StateMachineFactoryProps): StateMachineFactoryResponse
```

# StateMachineFactoryProps

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|stateMachineProps|[`sfn.StateMachineProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_stepfunctions.StateMachineProps.html)|The CDK properties that define the state machine. This property is required and must include a definitionBody or definition (definition is deprecated)|
|logGroup?|[]`logs.LogGroup`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_logs.LogGroup.html)|An existing LogGroup to which the new state machine will write log entries. Default: none, the construct will create a new log group.|

# StateMachineFactoryResponse

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|stateMachineProps|[`sfn.StateMachineProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_stepfunctions.StateMachineProps.html)||
|logGroup|[]`logs.LogGroupProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_logs.LogGroupProps.html)||

# Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

* An AWS Step Functions State Machine

  * Configured to log to the new log group at LogLevel.ERROR
* Amazon CloudWatch Logs Log Group

  * Log name is prefaced with /aws/vendedlogs/ to avoid resource policy [issues](https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html#cloudwatch-iam-policy). The Log Group name is still created to be unique to the stack to avoid name collisions.

# Architecture

![Architecture Diagram](sf-architecture.png)

---


© Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import constructs as _constructs_77d1e7e8


class ConstructsFactories(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.ConstructsFactories",
):
    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605983066d245d838df0751ca3d83223b93e3dac7281a9b7677ff8c39ccd96d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="s3BucketFactory")
    def s3_bucket_factory(
        self,
        id: builtins.str,
        *,
        bucket_props: typing.Any = None,
        logging_bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        log_s3_access_logs: typing.Optional[builtins.bool] = None,
    ) -> "S3BucketFactoryResponse":
        '''
        :param id: -
        :param bucket_props: -
        :param logging_bucket_props: -
        :param log_s3_access_logs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b90bfb94c5304484be85483634a7064b119ae1b0c5ed7cfc594e3e7bbf37f0)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3BucketFactoryProps(
            bucket_props=bucket_props,
            logging_bucket_props=logging_bucket_props,
            log_s3_access_logs=log_s3_access_logs,
        )

        return typing.cast("S3BucketFactoryResponse", jsii.invoke(self, "s3BucketFactory", [id, props]))

    @jsii.member(jsii_name="stateMachineFactory")
    def state_machine_factory(
        self,
        id: builtins.str,
        *,
        state_machine_props: typing.Union[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps, typing.Dict[builtins.str, typing.Any]],
        log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "StateMachineFactoryResponse":
        '''
        :param id: -
        :param state_machine_props: The CDK properties that define the state machine. This property is required and must include a definitionBody or definition (definition is deprecated)
        :param log_group_props: An existing LogGroup to which the new state machine will write log entries. Default: none, the construct will create a new log group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8ce2d58c9a66b894497fcb91691d41649f06370c9e15b72ef1373fbe0d05c6)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StateMachineFactoryProps(
            state_machine_props=state_machine_props, log_group_props=log_group_props
        )

        return typing.cast("StateMachineFactoryResponse", jsii.invoke(self, "stateMachineFactory", [id, props]))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.S3BucketFactoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_props": "bucketProps",
        "logging_bucket_props": "loggingBucketProps",
        "log_s3_access_logs": "logS3AccessLogs",
    },
)
class S3BucketFactoryProps:
    def __init__(
        self,
        *,
        bucket_props: typing.Any = None,
        logging_bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        log_s3_access_logs: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param bucket_props: -
        :param logging_bucket_props: -
        :param log_s3_access_logs: -
        '''
        if isinstance(logging_bucket_props, dict):
            logging_bucket_props = _aws_cdk_aws_s3_ceddda9d.BucketProps(**logging_bucket_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a251aca0d0848bcaeaed9669ce040e9bd9f304c875a3796313bd27abcdacc3)
            check_type(argname="argument bucket_props", value=bucket_props, expected_type=type_hints["bucket_props"])
            check_type(argname="argument logging_bucket_props", value=logging_bucket_props, expected_type=type_hints["logging_bucket_props"])
            check_type(argname="argument log_s3_access_logs", value=log_s3_access_logs, expected_type=type_hints["log_s3_access_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_props is not None:
            self._values["bucket_props"] = bucket_props
        if logging_bucket_props is not None:
            self._values["logging_bucket_props"] = logging_bucket_props
        if log_s3_access_logs is not None:
            self._values["log_s3_access_logs"] = log_s3_access_logs

    @builtins.property
    def bucket_props(self) -> typing.Any:
        result = self._values.get("bucket_props")
        return typing.cast(typing.Any, result)

    @builtins.property
    def logging_bucket_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps]:
        result = self._values.get("logging_bucket_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps], result)

    @builtins.property
    def log_s3_access_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("log_s3_access_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketFactoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.S3BucketFactoryResponse",
    jsii_struct_bases=[],
    name_mapping={"s3_bucket": "s3Bucket", "s3_logging_bucket": "s3LoggingBucket"},
)
class S3BucketFactoryResponse:
    def __init__(
        self,
        *,
        s3_bucket: _aws_cdk_aws_s3_ceddda9d.Bucket,
        s3_logging_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket] = None,
    ) -> None:
        '''
        :param s3_bucket: -
        :param s3_logging_bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e83545e4e90253a16e42d104a9338e2ce2020b20c95b614ea013e7c4918073)
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3_logging_bucket", value=s3_logging_bucket, expected_type=type_hints["s3_logging_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_bucket": s3_bucket,
        }
        if s3_logging_bucket is not None:
            self._values["s3_logging_bucket"] = s3_logging_bucket

    @builtins.property
    def s3_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.Bucket:
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Bucket, result)

    @builtins.property
    def s3_logging_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket]:
        result = self._values.get("s3_logging_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketFactoryResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.StateMachineFactoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "state_machine_props": "stateMachineProps",
        "log_group_props": "logGroupProps",
    },
)
class StateMachineFactoryProps:
    def __init__(
        self,
        *,
        state_machine_props: typing.Union[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps, typing.Dict[builtins.str, typing.Any]],
        log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param state_machine_props: The CDK properties that define the state machine. This property is required and must include a definitionBody or definition (definition is deprecated)
        :param log_group_props: An existing LogGroup to which the new state machine will write log entries. Default: none, the construct will create a new log group.
        '''
        if isinstance(state_machine_props, dict):
            state_machine_props = _aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps(**state_machine_props)
        if isinstance(log_group_props, dict):
            log_group_props = _aws_cdk_aws_logs_ceddda9d.LogGroupProps(**log_group_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ef38c5b8793990636642f918f311333d9be77dfc62aec7517d2993d778bdb1)
            check_type(argname="argument state_machine_props", value=state_machine_props, expected_type=type_hints["state_machine_props"])
            check_type(argname="argument log_group_props", value=log_group_props, expected_type=type_hints["log_group_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "state_machine_props": state_machine_props,
        }
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props

    @builtins.property
    def state_machine_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps:
        '''The CDK properties that define the state machine.

        This property is required and
        must include a definitionBody or definition (definition is deprecated)
        '''
        result = self._values.get("state_machine_props")
        assert result is not None, "Required property 'state_machine_props' is missing"
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps, result)

    @builtins.property
    def log_group_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroupProps]:
        '''An existing LogGroup to which the new state machine will write log entries.

        Default: none, the construct will create a new log group.
        '''
        result = self._values.get("log_group_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroupProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StateMachineFactoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-constructs-factories.StateMachineFactoryResponse",
    jsii_struct_bases=[],
    name_mapping={"log_group": "logGroup", "state_machine": "stateMachine"},
)
class StateMachineFactoryResponse:
    def __init__(
        self,
        *,
        log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
    ) -> None:
        '''
        :param log_group: The log group that will receive log messages from the state maching.
        :param state_machine: The state machine created by the factory (the state machine role is available as a property on this resource).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__161202dcfa7b7271dad8c07356c59eacd279fc41c1b984608b687fc4baf227f5)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group": log_group,
            "state_machine": state_machine,
        }

    @builtins.property
    def log_group(self) -> _aws_cdk_aws_logs_ceddda9d.ILogGroup:
        '''The log group that will receive log messages from the state maching.'''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.ILogGroup, result)

    @builtins.property
    def state_machine(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine:
        '''The state machine created by the factory (the state machine role is available as a property on this resource).'''
        result = self._values.get("state_machine")
        assert result is not None, "Required property 'state_machine' is missing"
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StateMachineFactoryResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ConstructsFactories",
    "S3BucketFactoryProps",
    "S3BucketFactoryResponse",
    "StateMachineFactoryProps",
    "StateMachineFactoryResponse",
]

publication.publish()

def _typecheckingstub__605983066d245d838df0751ca3d83223b93e3dac7281a9b7677ff8c39ccd96d4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b90bfb94c5304484be85483634a7064b119ae1b0c5ed7cfc594e3e7bbf37f0(
    id: builtins.str,
    *,
    bucket_props: typing.Any = None,
    logging_bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    log_s3_access_logs: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8ce2d58c9a66b894497fcb91691d41649f06370c9e15b72ef1373fbe0d05c6(
    id: builtins.str,
    *,
    state_machine_props: typing.Union[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps, typing.Dict[builtins.str, typing.Any]],
    log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a251aca0d0848bcaeaed9669ce040e9bd9f304c875a3796313bd27abcdacc3(
    *,
    bucket_props: typing.Any = None,
    logging_bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    log_s3_access_logs: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e83545e4e90253a16e42d104a9338e2ce2020b20c95b614ea013e7c4918073(
    *,
    s3_bucket: _aws_cdk_aws_s3_ceddda9d.Bucket,
    s3_logging_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ef38c5b8793990636642f918f311333d9be77dfc62aec7517d2993d778bdb1(
    *,
    state_machine_props: typing.Union[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachineProps, typing.Dict[builtins.str, typing.Any]],
    log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161202dcfa7b7271dad8c07356c59eacd279fc41c1b984608b687fc4baf227f5(
    *,
    log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
) -> None:
    """Type checking stubs"""
    pass
