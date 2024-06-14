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

import aws_cdk.aws_ecr as _aws_cdk_aws_ecr_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="@occmundial/occ-ecr-pattern.IEcrProps")
class IEcrProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.List[_aws_cdk_aws_iam_ceddda9d.IPrincipal]:
        ...

    @builtins.property
    @jsii.member(jsii_name="scanOnPush")
    def scan_on_push(self) -> builtins.bool:
        ...


class _IEcrPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@occmundial/occ-ecr-pattern.IEcrProps"

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.List[_aws_cdk_aws_iam_ceddda9d.IPrincipal]:
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.IPrincipal], jsii.get(self, "principals"))

    @builtins.property
    @jsii.member(jsii_name="scanOnPush")
    def scan_on_push(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "scanOnPush"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEcrProps).__jsii_proxy_class__ = lambda : _IEcrPropsProxy


class OCCEcrPattern(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@occmundial/occ-ecr-pattern.OCCEcrPattern",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: IEcrProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7579c72a580fc9427ca2407fcc2f2a46e52180d234a6f762b5c48abe0b9dc4f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="ecr")
    def ecr(self) -> _aws_cdk_aws_ecr_ceddda9d.IRepository:
        return typing.cast(_aws_cdk_aws_ecr_ceddda9d.IRepository, jsii.get(self, "ecr"))

    @ecr.setter
    def ecr(self, value: _aws_cdk_aws_ecr_ceddda9d.IRepository) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d615282b7ab45e72ba534fd991bc0e7703c5d86f660dca73297341538618dae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ecr", value)

    @builtins.property
    @jsii.member(jsii_name="ecrArn")
    def ecr_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ecrArn"))

    @ecr_arn.setter
    def ecr_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc45a2732d58da986a7411bdc1ef9a39dc0082dcf4e13a705c1e1b682f09f5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ecrArn", value)

    @builtins.property
    @jsii.member(jsii_name="ecrImageName")
    def ecr_image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ecrImageName"))

    @ecr_image_name.setter
    def ecr_image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7815bc1690f4e59044c37668a6d7b4e6e07c0afc74d4922b423840a23e450fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ecrImageName", value)


__all__ = [
    "IEcrProps",
    "OCCEcrPattern",
]

publication.publish()

def _typecheckingstub__d7579c72a580fc9427ca2407fcc2f2a46e52180d234a6f762b5c48abe0b9dc4f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IEcrProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d615282b7ab45e72ba534fd991bc0e7703c5d86f660dca73297341538618dae8(
    value: _aws_cdk_aws_ecr_ceddda9d.IRepository,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc45a2732d58da986a7411bdc1ef9a39dc0082dcf4e13a705c1e1b682f09f5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7815bc1690f4e59044c37668a6d7b4e6e07c0afc74d4922b423840a23e450fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
