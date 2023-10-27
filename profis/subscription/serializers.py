from datetime import timedelta
from typing import Any

from django.db.models import F, Q
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers

from profis.categories.models import Category
from profis.subscription.models import UserPlan


class UserPlanSerializer(serializers.ModelSerializer):
    plan_type = serializers.ChoiceField(choices=UserPlan.PlanType.choices)
    package_type = serializers.ChoiceField(choices=UserPlan.PackageType.choices)

    class Meta:
        model = UserPlan
        fields = ["id", "user", "categories", "plan_type", "package_type", "is_active"]


class UserPlanCreateSerializer(serializers.ModelSerializer):
    plan_type = serializers.ChoiceField(choices=UserPlan.PlanType.choices, write_only=True)
    package_type = serializers.ChoiceField(choices=UserPlan.PackageType.choices, write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, write_only=True)
    total_amount = serializers.DecimalField(max_digits=9, decimal_places=2, write_only=True)

    class Meta:
        model = UserPlan
        fields = [
            "id",
            "user",
            "plan_type",
            "categories",
            "package_type",
            "total_amount",
        ]

    def validate(self, validated_data):
        user = validated_data.get("user", None)
        total_amount = validated_data.get("total_amount", None)
        plan_type = validated_data.get("plan_type", None)
        categories = validated_data.get("categories", None)
        if not total_amount or total_amount <= 0:
            raise serializers.ValidationError(_("Введите общую сумму"))

        if user and total_amount:
            user_wallet = user.userwallet
            if total_amount > user_wallet.balance:
                raise serializers.ValidationError(_("Недостаточно средств"))

        if plan_type == UserPlan.PlanType.BASE:
            for category in categories:
                if category.get_level() != 1:
                    raise serializers.ValidationError(_("Разрешены только родительские категории"))

        return validated_data

    def create(self, validated_data) -> Any:
        categories = validated_data.pop("categories", None)
        plan_type = validated_data.pop("plan_type", None)
        package_type = validated_data.pop("package_type", None)
        user = validated_data["user"]
        responses = 0
        user_plans = []

        if categories and plan_type and package_type:
            if plan_type == UserPlan.PlanType.BASE:
                if package_type == UserPlan.PackageType.BASE_25:
                    responses += 25
                elif package_type == UserPlan.PackageType.BASE_50:
                    responses += 50
                elif package_type == UserPlan.PackageType.BASE_100:
                    responses += 100
                for category in categories:
                    filter_condition = Q(user=user, categories=category)

                    user_plan, created = UserPlan.objects.filter(filter_condition).get_or_create(
                        plan_type=plan_type,
                        defaults={
                            "user": user,
                            "categories": category,
                            "plan_type": plan_type,
                            "package_type": package_type,
                            "number_of_responses": responses,
                        },
                    )
                    if not created:
                        # Check plan status, if active extend expiration date otherwise count by current date.
                        if user_plan.is_active:
                            user_plan.number_of_responses = F("number_of_responses") + responses
                            user_plan.expired_at = F("expired_at") + timedelta(days=30)
                        else:
                            user_plan.number_of_responses = responses
                            user_plan.expired_at = timezone.now() + timedelta(days=30)

                        user_plan.save()
                    user_plans.append(user_plan)

            elif plan_type == UserPlan.PlanType.UNLIM:
                for category in categories:
                    filter_condition = Q(user=user, categories=category)

                    user_plan, created = UserPlan.objects.filter(filter_condition).get_or_create(
                        plan_type=plan_type,
                        defaults={
                            "user": user,
                            "categories": category,
                            "plan_type": plan_type,
                            "package_type": package_type,
                        },
                    )
                    if not created:
                        # Check plan status, if active extend expiration date otherwise count by current date.
                        if user_plan.is_active:
                            if package_type == UserPlan.PackageType.UNLIM_15:
                                user_plan.expired_at = F("expired_at") + timedelta(days=15)
                            elif package_type == UserPlan.PackageType.UNLIM_30:
                                user_plan.expired_at = F("expired_at") + timedelta(days=30)
                            elif package_type == UserPlan.PackageType.UNLIM_90:
                                user_plan.expired_at = F("expired_at") + timedelta(days=90)
                        else:
                            if package_type == UserPlan.PackageType.UNLIM_15:
                                user_plan.expired_at = timezone.now() + timedelta(days=15)
                            elif package_type == UserPlan.PackageType.UNLIM_30:
                                user_plan.expired_at = timezone.now() + timedelta(days=30)
                            elif package_type == UserPlan.PackageType.UNLIM_90:
                                user_plan.expired_at = timezone.now() + timedelta(days=90)
                        user_plan.save()

                    user_plans.append(user_plan)

        return user_plans
