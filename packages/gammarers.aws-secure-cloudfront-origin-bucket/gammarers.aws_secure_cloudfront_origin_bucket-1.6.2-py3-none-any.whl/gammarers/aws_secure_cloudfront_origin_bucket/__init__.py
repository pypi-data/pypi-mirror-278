'''
# AWS Secure CloudFront Origin Bucket (for CDK v2)

[![GitHub](https://img.shields.io/github/license/gammarers/aws-secure-cloudfront-origin-bucket?style=flat-square)](https://github.com/gammarers/aws-secure-cloudfront-origin-bucket/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarers/aws-secure-cloudfront-origin-bucket?style=flat-square)](https://www.npmjs.com/package/@gammarers/aws-secure-cloudfront-origin-bucket)
[![PyPI](https://img.shields.io/pypi/v/gammarers.aws-secure-cloudfront-origin-bucket?style=flat-square)](https://pypi.org/project/gammarers.aws-secure-cloudfront-origin-bucket/)
[![Nuget](https://img.shields.io/nuget/v/Gammarers.CDK.AWS.SecureCloudFrontOriginBucket?style=flat-square)](https://www.nuget.org/packages/Gammarers.CDK.AWS.ScureCloudFrontOriginBucket/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarers/aws-secure-cloudfront-origin-bucket/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarers/aws-secure-cloudfront-origin-bucket/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarers/aws-secure-cloudfront-origin-bucket?sort=semver&style=flat-square)](https://github.com/gammarers/aws-secure-cloudfront-origin-bucket/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarers/aws-secure-cloudfront-origin-bucket)](https://constructs.dev/packages/@gammarers/aws-secure-cloudfront-origin-bucket)

An AWS CDK construct library to create secure S3 buckets for CloudFront origin.

## Install

### TypeScript

#### install by npm

```shell
npm install @gammarers/aws-secure-cloudfront-origin-bucket
```

#### install by yarn

```shell
yarn add @gammarers/aws-secure-cloudfront-origin-bucket
```

#### install by pnpm

```shell
pnpm add @gammarers/aws-secure-cloudfront-origin-bucket
```

#### install by bun

```shell
bun add @gammarers/aws-secure-cloudfront-origin-bucket
```

### Python

```shell
pip install gammarers.aws-secure-cloudfront-origin-bucket
```

### C# / .NET

```shell
dotnet add package gammarers.CDK.AWS.SecureCloudFrontOriginBucket
```

## Example

### for OAI(Origin Access Identity)

```python
import { SecureCloudFrontOriginBucket, SecureCloudFrontOriginType } from '@gammarers/aws-secure-cloudfront-origin-bucket';

const oai = new cloudfront.OriginAccessIdentity(stack, 'OriginAccessIdentity');

new SecureCloudFrontOriginBucket(stack, 'SecureCloudFrontOriginBucket', {
  bucketName: 'example-origin-bucket',
  cloudFrontOriginType: SecureCloudFrontOriginType.ORIGIN_ACCESS_IDENTITY,
  cloudFrontOriginAccessIdentityS3CanonicalUserId: oai.cloudFrontOriginAccessIdentityS3CanonicalUserId,
});
```

### for OAC(Origin Access Control)

```python
import { SecureCloudFrontOriginBucket, SecureCloudFrontOriginType } from '@gammarers/aws-secure-cloudfront-origin-bucket';

declare const distribution: cloudfront.Distribution;

new SecureCloudFrontOriginBucket(stack, 'SecureCloudFrontOriginBucket', {
  bucketName: 'example-origin-bucket',
  cloudFrontOriginType: SecureCloudFrontOriginType.ORIGIN_ACCESS_CONTROL,
  cloudFrontArn: `arn:aws:cloudfront::123456789:distribution/${distribution.distributionId}`,
});
```

## License

This project is licensed under the Apache-2.0 License.
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

import constructs as _constructs_77d1e7e8
import gammarers.aws_secure_bucket as _gammarers_aws_secure_bucket_0aa7e232


@jsii.data_type(
    jsii_type="@gammarers/aws-secure-cloudfront-origin-bucket.SecureCloudFrontOriginAccessControlBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_front_arn": "cloudFrontArn",
        "cloud_front_origin_type": "cloudFrontOriginType",
        "bucket_name": "bucketName",
    },
)
class SecureCloudFrontOriginAccessControlBucketProps:
    def __init__(
        self,
        *,
        cloud_front_arn: builtins.str,
        cloud_front_origin_type: "SecureCloudFrontOriginType",
        bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_front_arn: 
        :param cloud_front_origin_type: 
        :param bucket_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa453332664bc4fb3511b18f5bf5f05baccf5b7ea74a049133d6dcce58d3da1c)
            check_type(argname="argument cloud_front_arn", value=cloud_front_arn, expected_type=type_hints["cloud_front_arn"])
            check_type(argname="argument cloud_front_origin_type", value=cloud_front_origin_type, expected_type=type_hints["cloud_front_origin_type"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_front_arn": cloud_front_arn,
            "cloud_front_origin_type": cloud_front_origin_type,
        }
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name

    @builtins.property
    def cloud_front_arn(self) -> builtins.str:
        result = self._values.get("cloud_front_arn")
        assert result is not None, "Required property 'cloud_front_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_front_origin_type(self) -> "SecureCloudFrontOriginType":
        result = self._values.get("cloud_front_origin_type")
        assert result is not None, "Required property 'cloud_front_origin_type' is missing"
        return typing.cast("SecureCloudFrontOriginType", result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureCloudFrontOriginAccessControlBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gammarers/aws-secure-cloudfront-origin-bucket.SecureCloudFrontOriginAccessIdentityBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_front_origin_access_identity_s3_canonical_user_id": "cloudFrontOriginAccessIdentityS3CanonicalUserId",
        "cloud_front_origin_type": "cloudFrontOriginType",
        "bucket_name": "bucketName",
    },
)
class SecureCloudFrontOriginAccessIdentityBucketProps:
    def __init__(
        self,
        *,
        cloud_front_origin_access_identity_s3_canonical_user_id: builtins.str,
        cloud_front_origin_type: "SecureCloudFrontOriginType",
        bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_front_origin_access_identity_s3_canonical_user_id: 
        :param cloud_front_origin_type: 
        :param bucket_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35443b3704c8e899447eb2e035faf6589baef0d046d23a80b8688398f703bc80)
            check_type(argname="argument cloud_front_origin_access_identity_s3_canonical_user_id", value=cloud_front_origin_access_identity_s3_canonical_user_id, expected_type=type_hints["cloud_front_origin_access_identity_s3_canonical_user_id"])
            check_type(argname="argument cloud_front_origin_type", value=cloud_front_origin_type, expected_type=type_hints["cloud_front_origin_type"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_front_origin_access_identity_s3_canonical_user_id": cloud_front_origin_access_identity_s3_canonical_user_id,
            "cloud_front_origin_type": cloud_front_origin_type,
        }
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name

    @builtins.property
    def cloud_front_origin_access_identity_s3_canonical_user_id(self) -> builtins.str:
        result = self._values.get("cloud_front_origin_access_identity_s3_canonical_user_id")
        assert result is not None, "Required property 'cloud_front_origin_access_identity_s3_canonical_user_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_front_origin_type(self) -> "SecureCloudFrontOriginType":
        result = self._values.get("cloud_front_origin_type")
        assert result is not None, "Required property 'cloud_front_origin_type' is missing"
        return typing.cast("SecureCloudFrontOriginType", result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureCloudFrontOriginAccessIdentityBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecureCloudFrontOriginBucket(
    _gammarers_aws_secure_bucket_0aa7e232.SecureBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarers/aws-secure-cloudfront-origin-bucket.SecureCloudFrontOriginBucket",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union[typing.Union[SecureCloudFrontOriginAccessControlBucketProps, typing.Dict[builtins.str, typing.Any]], typing.Union[SecureCloudFrontOriginAccessIdentityBucketProps, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761879e9e87fc67cd681f9978d9a5f4b6a8d712092bc8cc46f6a90f3f42ac4f1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])


@jsii.enum(
    jsii_type="@gammarers/aws-secure-cloudfront-origin-bucket.SecureCloudFrontOriginType"
)
class SecureCloudFrontOriginType(enum.Enum):
    ORIGIN_ACCESS_IDENTITY = "ORIGIN_ACCESS_IDENTITY"
    '''OriginAccessIdentity.'''
    ORIGIN_ACCESS_CONTROL = "ORIGIN_ACCESS_CONTROL"
    '''OriginAccessControl.'''


__all__ = [
    "SecureCloudFrontOriginAccessControlBucketProps",
    "SecureCloudFrontOriginAccessIdentityBucketProps",
    "SecureCloudFrontOriginBucket",
    "SecureCloudFrontOriginType",
]

publication.publish()

def _typecheckingstub__aa453332664bc4fb3511b18f5bf5f05baccf5b7ea74a049133d6dcce58d3da1c(
    *,
    cloud_front_arn: builtins.str,
    cloud_front_origin_type: SecureCloudFrontOriginType,
    bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35443b3704c8e899447eb2e035faf6589baef0d046d23a80b8688398f703bc80(
    *,
    cloud_front_origin_access_identity_s3_canonical_user_id: builtins.str,
    cloud_front_origin_type: SecureCloudFrontOriginType,
    bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761879e9e87fc67cd681f9978d9a5f4b6a8d712092bc8cc46f6a90f3f42ac4f1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Union[typing.Union[SecureCloudFrontOriginAccessControlBucketProps, typing.Dict[builtins.str, typing.Any]], typing.Union[SecureCloudFrontOriginAccessIdentityBucketProps, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass
