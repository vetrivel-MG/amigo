metaprompt_template= """
    Instruction:

    The below given informations are the collection name and its discription stored in Qdrant database.
    Refer the following and provide relavent answers based on the questions asked.

        COLLECTION NAME: AdvisorDocument 
            • Collection Explanation: This collection is used to store the recommendation data from the azure portal. 
            • Important fields: Some important fields in this collection are subscitionId, category, impactedField, ImpactedValue, recommendationTypeId. 
        
        COLLECTION NAME: AWSBudget 
            • Collection Explanation: This collection is used to store the aws budget related values.  
            • Important fields: Some important fields in this table are budgetName, timeUnit, budgetType etc... 

        COLLECTION NAME: AWSCostAndUsage 
            • Collection Explanation: The cost usage collection is used to store the cost and usage details of the AWS resources. 
            • Important fields: Some important fields in this collection are accountId, total etc.. 
        
        COLLECTION NAME: AWSCostAndUsageMonthly 
            • Collection Explanation: This table is same as the AWScostAndUsage, but here the monthly data is calculated. 
            • Important fields: Some important fields in this collection are accountId, total etc.. 
        
        COLLECTION NAME: AWSCostForecast 
            • Collection Explanation: This collection is used to store the predicted values from AWS and use it in the saaspe when needed. 
            • Important fields: predictionIntervalLowerBound, predictionIntervalUpperBound, totalCost are some important fields from this table. 
        
        COLLECTION NAME: AWSResourcesDocument 
            • Collection Explanation: This collection is used to store resource details from the AWS portal. 
            • Important fields:resourceARN, region and accountId are some important fields in this coollection. 
        
        COLLECTION NAME: AWSRightSizingRecommendationDocument 
            • Collection Explanation: This collection is used to store the rightsizing recomendation details from the AWS portal, then use it in saaspe when required. 
            • Important fields: rightsizingType, modifyRecommendationDetail are some important fields in this collection. 
        
        COLLECTION NAME: AzureBudgets 
            • Collection Explanation: This collection is used to store the data when the super admin from the saaspe creates a budget in azure, in super admin access from saaspe. 
            • Important fields: Some important fields in this collection are budgetId, name, category, amount etc... 
        
        COLLECTION NAME: AzureCostAndUsageByServiceName 
            • Collection Explanation: This collection is used to store the cost and usage details of different services in the saaspe application. 
            • Important fields: Some important fields in this collection are name, type, subscriptionId etc... 
        
        COLLECTION NAME: AzureCostManagementQuery 
            • Collection Explanation: This collection is used to store and manage cost details related to the azure portal.  
            • Important fields: SubscriptionId, type, name are some important fields of this collection. 
        
        COLLECTION NAME: AzureCostManagementQueryMonthlyDocument 
            • Collection Explanation: This collection is used to store and manage the azure cost-related details that need to be queried monthly. 
            • Important fields: Some important fields in this collection are SubcriptionId, name, createdOn etc... 
        
        COLLECTION NAME: AzureCostManagementQueryQuaterlyDocument 
            • Collection Explanation: This collection is used to store and manage the azure cost-related details that need to be queried on a quarterly basis. 
            • Important fields: Some important fields of this collection are SubscriptionId, name, CreatedOn, updatedOn etc... 
        
        COLLECTION NAME: AzureCostManagementQueryYearlyDocument 
            • Collection Explanation: This collection is used to store and manage the azure cost-related details that need to be queried on a yearly basis. 
            • Important fields: Some important fields of this collection are SubscriptionId, name, CreatedOn, updatedOn etc... 
        
        COLLECTION NAME: AzureForecast  
            • Collection Explanation: The.AzureForecast collection is used for storing historical data, models, or forecasts related to Azure services, which could be used for planning, budgeting, or optimizing cloud resources. 
            • Important fields: resourceName, name and subscriptionId are some important fields of this collection. 
        
        COLLECTION NAME: AzureResourceGroup 
            • Collection Explanation: The AzureResourceGroup collection organizes Azure resource group data, aiding in effective resource management within cloud development projects, enabling monitoring and optimization of resource usage. 
            • Important fields: name, location, provisioningState and subscriptioId are some importanr fields of this collection.  
    
        COLLECTION NAME: AzureResources 
            • Collection Explanation: This collection contains data pertaining to various Azure resources deployed within cloud environments. 
            • Important fields: resourcegroupId, clientId, resourceId annd location are some important fields of this collection. 
        
        COLLECTION NAME: AzureSubscriptions 
            • Collection Explanation: his collection stores data related to Azure subscriptions, including subscription IDs, display names, client IDs, and timestamps. 
            • Important fields: resourcegroupId, clientId, resourceId, and location are key attributes within this collection, providing essential details about Azure resources, their associated clients, unique identifiers, and geographical deployment locations. 
        
        COLLECTION NAME: ConversationDocument 
            • Collection Explanation: This collection stores structured data related to conversations, including conversation IDs, user IDs, user emails, queries, responses, timestamps, and class information. 
            • Important fields: conversationId, userId, userEmail, query, response, and createdOn are crucial attributes within this collection, providing essential details about the conversations, users involved, queries raised, responses given, and timestamps of interaction. 
        
        COLLECTION NAME: ResourceGroupsActualCostDocument 
            • Collection Explanation: This collection stores structured data regarding actual costs associated with Azure resource groups, utilizing Microsoft.CostManagement/query type, linked to specific subscription IDs. 
            • Important fields: name, type, subscriptionId, column, rows, updatedOn, and _class are crucial for resource group identification, cost management type, associated subscription, dataset structure, actual cost data, last update timestamp, and document classification. 
        
        COLLECTION NAME: database_sequences 
            • Collection Explanation: This collection manages sequences for various documents within the database, aiding in unique identifier generation. 
            • Important fields: Each "_id" corresponds to a specific document type, with its associated "seq" indicating the sequence number used for generating unique identifiers. These sequences ensure systematic document identification and management within the database. 
        
        COLLECTION NAME: saaspe_adaptor_user_details 
            • Collection Explanation: This collection stores details about users utilizing adaptors, including their email addresses and associated application details. 
            • Important fields: userEmail, fields (containing applicationName, applicationId, and userId), and _class. These fields provide crucial information about users' email addresses, associated applications, and the class of the document within the data model. 
         

        COLLECTION NAME: database_sequences 
            • Collection Explanation: This collection manages sequences for different documents within the marketplace database, aiding in the generation of unique identifiers. 
            • Important fields: _id and seq. Each "_id" corresponds to a specific document type, with its associated "seq" indicating the sequence number used for generating unique identifiers. These sequences ensure systematic document identification and management within the marketplace database. 
        
        COLLECTION NAME: product-items 
        • Collection Explanation: This collection stores information about various product items, providing details such as logos, titles, descriptions, UUIDs, ratings, categories, and subcategories. 
        • Important fields: _id, logo, title, description, UUID, rating, category, subCategory, and __v. These contain essential information about product items for effective management and presentation. 
        
        COLLECTION NAME: product-reviews 
            • Collection Explanation: This collection stores reviews for products, including details such as vendor ID, vendor name, reviewer name, designation, company details, rating, review date, UUID, and extended review. 
            • Important fields: vendorId, vendorName, name, designation, companyDetails, rating, ratedOn, UUID, review, and extendedReview. These fields provide crucial information about product reviews, including reviewer details, ratings, and extended feedback for effective product assessment. 
        
    
        COLLECTION NAME: AuditEventDocument 
            • Collection Explanation: This collection logs audit events, capturing details like creation and update timestamps, start date, envelope ID, and associated event fields. 
            • Important fields: _id, createdOn, updatedOn, startDate, envelopeId, and auditEvents. These fields provide crucial information about audit events, including timestamps, event details, and associated envelope information for tracking actions within the system. 
        
        COLLECTION NAME: CentralRepoDocument 
            • Collection Explanation: This collection stores documents related to a central repository, with each document containing details such as the repository name and associated envelope ID. 
            • Important fields: _id, repositoryName, envelopeId, and _class. These fields provide essential information about documents stored in the central repository, including unique identifiers, repository names, envelope IDs, and document classes within the data model. 
        
        COLLECTION NAME: ClmContractDocument 
            • Collection Explanation: Manages contract documents with key details including creation date, contract name, start and end dates, renewal reminders, template and envelope IDs, sender's details, status, and modification dates. 
            • Important fields: _id, createdOn, contractName, contractStartDate, contractEndDate, renewalReminderNotification, templateId, envelopeId, senderEmail, senderName, status, lastModifiedDateTime, and startDate. These fields are vital for contract management. 
        
        COLLECTION NAME: ClmTemplateDocument 
            • Collection Explanation: Stores templates with details such as template ID and name. 
            • Important fields: _id, templateId, and templateName. 
        
        COLLECTION NAME: EnvelopeDocument 
            • Collection Explanation: Stores envelope details including access control settings, comment permissions, markup allowances, reassignment permissions, viewing history access, attachments URI, brand ID, certificate URI, and completion date. 
            • Important fields: _id, envelope, accessControlListBase64, allowComments, allowMarkup, allowReassign, allowViewHistory, attachmentsUri, brandId, certificateUri, and completedDateTime. 
        
        COLLECTION NAME: EventDocument 
            • Collection Explanation: Records events such as recipient completion and envelope sending, including details like event type, API version, URI, retry count, configuration ID, generated date time, data such as account and user IDs, envelope ID, recipient ID, creation and start dates. 
            • Important fields: _id, event, apiVersion, uri, retryCount, configurationId, generatedDateTime, data, accountId, userId, envelopeId, recipientId, createdOn, startDate. 
        
        COLLECTION NAME: ReviewerDocument 
            • Collection Explanation: Stores reviewer details for document reviews, including email, completion status, envelope ID, routing order, document version, order flag, and creator's email. 
            • Important fields: _id, email, isCompleted, envelopeId, routingOrder, docVersion, orderFlag, createdBy. 
        
        COLLECTION NAME: WorkFlowCreatorDocument 
            • Collection Explanation: Stores workflow details created by users, including email, pending recipients, envelope ID, contract name, flow type, and creation timestamp. 
            • Important fields: _id, email, pendingWith, envelopeId, contractName, flowType, createdOn.
 
 
    """ 