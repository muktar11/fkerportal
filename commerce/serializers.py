from rest_framework import serializers
from .models import SalesOrder, MakePayment, CSOAdmin, SDMOrderApprove, AADDSalesOrder, SalesOrderVerification, SalesOrderApprove, AADDSalesOrderVerification, SetPrice

class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrder
        fields = ('customer_name', 'Plate_number', 'sales_Route', 'Q', 'H', 'ONE', 'TWO', 'SubTotal', 'TransportationFee', 'Total')

class MakePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakePayment
        fields = ('payment', 'recipant')

class CSOAdminSerializer(serializers.ModelSerializer):
    OrdersPurchased = MakePaymentSerializer()

    class Meta:
        model = CSOAdmin
        fields = ('name', 'OrdersPurchased', 'is_processed')

class SDMOrderApproveSerializer(serializers.ModelSerializer):
    process = CSOAdminSerializer()

    class Meta:
        model = SDMOrderApprove
        fields = ('name', 'process', 'is_approved')

class AADDSalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AADDSalesOrder
        fields = ('customer_name', 'Plate_number', 'SalesPerson', 'sales_Route', 'Q', 'H', 'ONE', 'TWO')

class SalesOrderVerificationSerializer(serializers.ModelSerializer):
    Payment = SDMOrderApproveSerializer()

    class Meta:
        model = SalesOrderVerification
        fields = ('Name', 'Payment', 'CSI_CSRI', 'Amount', 'BankName', 'BankRefNum', 'DepositDate', 'is_payed', 'is_available')

class SalesOrderApproveSerializer(serializers.ModelSerializer):
    Approves = SalesOrderVerificationSerializer()

    class Meta:
        model = SalesOrderApprove
        fields = ('SMD_NAME', 'Approves', 'is_approved')

class AADDSalesOrderVerificationSerializer(serializers.ModelSerializer):
    Payment = SDMOrderApproveSerializer()

    class Meta:
        model = AADDSalesOrderVerification
        fields = ('Name', 'SalesPerson', 'PlateNumber', 'Payment', 'CSI_CSRI', 'Amount', 'BankName', 'BankRefNum', 'DepositDate', 'is_payed', 'is_available')

class SetPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetPrice
        fields = ('Name', 'sales_Route', 'TransportationFee', 'Q', 'H', 'ONE', 'TWO')