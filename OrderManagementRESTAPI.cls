@RestResource(urlMapping='/OrderManagement/*')
global with sharing class OrderManagementRESTAPI {

    @HttpDelete
    global static void doDelete() {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;
        String accountId = req.requestURI.substring(req.requestURI.lastIndexOf('/')+1);
        Account account = [SELECT Id FROM Account WHERE Id = :accountId];
        delete account;
    }
  
    @HttpGet
    global static Order doGetOrder() {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;
        String orderId = req.requestURI.substring(req.requestURI.lastIndexOf('/')+1);
        List<Order> lstOrder = [SELECT Id, TotalAmount, AccountId, Account.Name, EffectiveDate, ContractId, Contract.ContractNumber FROM Order WHERE Id = :orderId LIMIT 1];
        if(lstOrder != null && lstOrder.size() > 0){
            return lstOrder[0];
        }
        return null;
    }
  
    @HttpPost
    global static String doPostAccount(String name, String phone, String website) {
        Account account = new Account();
        account.Name = name;
        account.phone = phone;
        account.website = website;
        insert account;
        return account.Id;
    }

    @HttpPut
    global static String doPutOrderItem(Decimal unitPrice, Decimal quantity, String orderItemId) {
        if(orderItemId != null && (unitPrice != null || quantity != null)){
            OrderItem orderItem = new OrderItem(Id=orderItemId);
            orderItem.UnitPrice = unitPrice;
            orderItem.Quantity = quantity;
            update orderItem;
            return orderItem.Id;
        }
        return 'No Records Found';        
    }
}
