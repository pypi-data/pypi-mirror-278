use std::collections::HashMap;
use lazy_static::lazy_static;

lazy_static! {
    pub static ref PIPELINE_BLACKLIST: HashMap<&'static str, bool> = {
        let mut map = HashMap::new();
        map.insert("", true);
        map.insert("Holded\\Banking\\Domain\\Institution\\Events\\ConnectionUpdatedEvent",true);
        map.insert("Holded\\Account\\Domain\\Account\\Events\\TrialExpiredEvent",true);
        map.insert("Holded\\Accounting\\Domain\\Ledger\\Events\\LedgerNumberedEvent",true);
        map.insert("Holded\\Banking\\Domain\\Transaction\\Events\\TransactionFxRateForcedEvent",true);
        map.insert("Holded\\Booking\\Domain\\Booking\\Events\\BookingNotificationStatusUpdatedEvent",true);
        map.insert("Holded\\Calendar\\Domain\\Activity\\Events\\ActivityConferencingCreatedEvent",true);
        map.insert("Holded\\Calendar\\Domain\\Activity\\Events\\ActivityCreatedEvent",true);
        map.insert("Holded\\Calendar\\Domain\\Activity\\Events\\ActivityDeletedEvent",true);
        map.insert("Holded\\Calendar\\Domain\\Calendar\\Events\\CalendarCreatedEvent",true);
        map.insert("Holded\\Ecommerce\\PluginConnector\\Domain\\Ecommerce\\Events\\ShopCreatedEvent",true);
        map.insert("Holded\\Invoicing\\Domain\\Ticketbai\\Events\\DocumentProviderIdAssignedEvent",true);
        map.insert("Holded\\Invoicing\\Domain\\Ticketbai\\Events\\DocumentSignedEvent",true);
        map.insert("Holded\\Platform\\Domain\\Billing\\Invoice\\Event\\InvoiceCreditNoteRegisteredEvent",true);
        map.insert("Holded\\Platform\\Domain\\Billing\\Invoice\\Event\\InvoiceRegisteredAsSalesInvoiceEvent",true);
        map.insert("Holded\\Platform\\Domain\\Billing\\Invoice\\Event\\InvoiceRegisteredInFinanceEvent",true);
        map.insert("Holded\\Platform\\Domain\\Sso\\Events\\SsoLoginInitializedEvent",true);
        map.insert("Holded\\Accounting\\Domain\\Analytical\\AnalyticalDailyEntriesRefreshedEvent",true);
        map.insert("Holded\\Mailing\\Domain\\Mailing\\MailingLogCreatedEvent",true);
        map.insert("Holded\\Mailing\\Domain\\Mailing\\Events\\MailingLogCreatedEvent",true);
        map
    };
}


lazy_static! {
    pub static ref SSGTM_BLACKLIST: HashMap<&'static str, bool> = {
        let mut map = HashMap::new();
        map.insert("Holded\\Product\\Domain\\Product\\Events\\ProductImageRemovedEvent", true);
        map.insert("Holded\\Product\\Domain\\Product\\Events\\PurchasePriceUpdatedEvent", true);
        map.insert("Holded\\Product\\Domain\\HistoricalCost\\Events\\VariantProductCostChangedEvent", true);
        map.insert("Holded\\Product\\Domain\\Product\\Variants\\Events\\VariantProductCreatedEvent", true);
        map.insert("Holded\\Product\\Domain\\HistoricalCost\\Events\\HistoricalCostCreatedEvent", true);
        map.insert("Holded\\Accounting\\Domain\\Entry\\Events\\AccountingEntryCreatedEvent", true);
        map.insert("Holded\\Inbox\\Domain\\Email\\Events\\EmailCreatedEvent", true);
        map.insert("Holded\\Accounting\\Domain\\Entry\\Events\\AccountingEntryRemovedEvent", true);
        map.insert("Holded\\Invoicing\\Domain\\Documents\\Events\\DocumentCreatedEvent", true);
        map.insert("Holded\\Invoicing\\Domain\\Documents\\Events\\DocumentUpdatedEvent", true);
        map.insert("Holded\\Product\\Domain\\Product\\Events\\ProductUpdatedEvent", true);
        map
    };
}