=========================================
Tools That Integrate with ActionKit
=========================================

Other vendors and ActionKit clients have used our APIs to integrate with their tools or to build functionality on top of ActionKit.  This list is for your information - we weren't involved in developing any of these tools (although some of them sound pretty cool), we haven't tested the code, etc.  

Please let us know if there are other links we should add to these lists.

.. Note::
  ActionKit generates API keys through a staff user and password. To give a
  vendor API access, set up a `staff account </dash/staff>`_ with "Active Account" 
  checked. You may add the account to the "All Models - View, Edit, and Delete"
  permission group to grant access to *all data* in the database, though this
  should only be done for a trusted partner. We do not recommend checking the
  "Admin Interface" or "Superuser Status" boxes. Send credentials for this account
  to the vendor using `One Time Secret <https://www.onetimesecret.com>`_ 
  or equivalent for security.

Vendor-managed Integrations
~~~~~~~~~~~~~

Contact the vendor below for additional information on their products and what their integration with ActionKit provides.


.. actblue

.. raw:: html

   <style>
       pre {
           word-wrap: break-word;
           overflow-wrap: break-word;
           white-space: pre-wrap;
       }
       .admonition ul,
       div.admonition ul {
           list-style-type: disc !important;
           margin-left: 0px !important;
           padding-left: 25px !important;
       }
       .admonition li,
       div.admonition li {
           display: list-item !important;
           list-style-type: disc !important;
           list-style-position: outside !important;
           margin-bottom: 10px !important;
           padding-left: 5px !important;
       }
       .image-with-margin {
           margin: 25px auto !important;
           display: block !important;
       }
   </style>

ActBlue
*******

.. admonition:: vendor-managed integration

   `ActBlue <https://secure.actblue.com/>`_ is a non-profit, building fundraising technology for the left. Their mission is to democratize power and help small-dollar donors make their voices heard in a real way.

   The integration automatically adds your donation data from ActBlue to your ActionKit database. The donations are pushed through as actual transactions against an import stub payment account so that you can use your regular donation reports for both native ActionKit and ActBlue donation data.

   **Installation**

   In order to use the ActBlue integration, you need to first make a few changes on the ActionKit side:

   * Configure one or more `stub accounts </admin/core/paymentaccount/>`_ to match your ActBlue accounts. Check the "actblue_webhook" so we know it's associated with ActBlue, and to show these instructions customized for the new account. If you only have a single ActBlue account, your instance already includes a "Default ActBlue" account. If you have multiple ActBlue accounts, you can create stub accounts in ActionKit to correspond to each of your ActBlue accounts.

   * Create `custom user fields </admin/core/alloweduserfield/>`_ named "employer", "occupation", and "express_lane" if these don't exist in your instance.

   * Set up a `staff account </dash/staff>`_ with "Active Account" checked. This account will only be used by the ActBlue webhook you create in the next step. We recommend that you do **NOT** check the *"Admin Interface"* or *"Superuser Status"* boxes.

   * Log into your ActBlue account and begin creation of a webhook using the form on their site. Detailed instructions can be found `here <https://support.actblue.com/campaigns/the-dashboard/setting-up-a-webhook-integration/#request>`_.

   * Select "ActBlue Default" as the webhook type. Username and password will use the info from the staff account you created. For the endpoint URL follow this format:

     .. raw:: html

        <pre>https://[your actionkit hostname]/webhooks/actblue/payments/?account=Default%20ActBlue&backfill=1</pre>

   (if necessary replace `Default%20ActBlue` with your account name, using `%20` to indicate spaces). This webhook will be used for one-time and recurring donations.

   * To set up webhooks for refunds and cancellations follow the steps above, but select "ActBlue Default Refunds" and "ActBlue Default Cancellations", respectively. For both types you will use the same username, password, and endpoint URL you used in the last step.

   * Finally, when you are ready to start processing ActBlue donations, you can turn on `ActBlue event processing </dash/config/edit/ActBlue%20Webhook/>`_.

   * If you would like to backfill historical donations, ask ActBlue to do this and to pass the backfill parameter when doing so (and to turn it off after the backfill is complete). This will avoid resubscribing users who have unsubscribed or bounced. Using the example endpoint above as a starting point, the backfill URL would be:

     .. raw:: html

        <pre>https://[your actionkit hostname]/webhooks/actblue/payments/?account=[account info used for endpoint URL]&backfill=1</pre>

   **Integration Notes**

   * To track ActBlue donations back to mailings, ActionKit relies on the refcode or refcode2 parameter being available in your mailings' links. If you use both of these parameters, donations will still flow from ActBlue to ActionKit correctly, but they will not be tracked back to a mailing. If you set a refcode value on your links, the value will be used as the source for the donation actions created in ActionKit.
   
   * ActionKit will alert you if we detect that there have been multiple failed attempts to connect to the ActBlue webhook. Admin staff users assigned as technical contacts will see on-screen warnings, and email alerts will be sent to the technical contacts defined under "Contact Settings" on the "Configure ActionKit" screen. If no technical contacts are set, we'll email the last two superusers to log in.
   
   .. image:: https://s3.us-east-1.amazonaws.com/clientcon/images/editor-2024-02-13-3.png
      :alt: ActBlue Integration Screenshot
      :width: 600px
      :align: center
      :class: image-with-margin
   
   * The ActBlue sync uses an ActionKit staff user to deliver webhooks. If someone edits one of these users, a warning will force them to acknowledge that the user is used by ActBlue before saving.
   
   .. image:: https://s3.us-east-1.amazonaws.com/clientcon/images/editor-2024-02-13-5.png
      :alt: ActBlue Warning Screenshot
      :width: 600px
      :align: center
      :class: image-with-margin
      
.. end_actblue

CallPower
****************

.. admonition:: vendor-managed integration

   `CallPower <http://callpower.org/>`_ enables click-to-call capability for your call pages and packages it with an admin backend for setting up and tracking your calls. Easily set up calls to Congress and custom targets, record and save message prompts, and see stats for each campaign and target.

ControlShift
****************

.. admonition:: vendor-managed integration

   `ControlShift <http://www.controlshiftlabs.com/>`_ is a set of web tools that helps progressive organizations build community, leadership and real power among their members. Their white-labeled distributed organizing toolset empowers your supporters to start, run, and win their own campaigns, with support from your organization. In addition to campaigns, ControlShift also supports member-created events, local groups, and donations. User and action data – including campaign signatures, event RSVPs, and donations - are automatically added to your AK database.

   Learn more here: https://controlshiftlabs.zendesk.com/hc/en-us/articles/203066966-ActionKit.

   ControlShift has also added an integration with VisitThem.org. VisitThem allows you to coordinate drop-in office visit at congressional district offices, recruit attendees for official public congressional events and stage in-person petition deliveries. It's self-service to setup, then attendee data for events flows automatically into ActionKit event campaigns -- no need to manually upload attendee data back into ActionKit. 

Grassroots Unwired
*********************

.. admonition:: vendor-managed integration

   Grassroots Unwired is built on the philosophy that mobile-first technology can be customized and utilized for the greater good. From helping progressive candidates win elections to empowering non-profit organizations working to save our environment, balance inequality and improve our communities. Grassroots Unwired bridges historical grassroots organizing with groundbreaking mobile technology.

   Use the `Grassroots Unwired <http://grassrootsunwired.com/>`_ mobile canvassing platform to collect data through face-to-face interactions by having people sign a petition, make a donation or choose to opt-in to a campaign. The Grassroots Unwired/ActionKit integration seamlessly redirects  the data from those face-to-face engagements to your ActionKit database and one or more Action Pages based on the results of the interaction. This integration can be set up through our rapid application design process so we can get you up and running quickly. 

MobilizeAmerica
*************************

.. admonition:: vendor-managed integration

   `MobilizeAmerica <https://www.mobilizeamerica.io/>`_  is an events and action platform that enables easy confirm and reshifting automation and cross-promotion with your partners. Hundreds of Democratic campaigns and national progressive organizations use MobilizeAmerica to recruit volunteers and drive them to action via a single collaborative platform. 

   Our ActionKit integration allows you to sync events and sign-ups into your ActionKit; as well as sync your events from ActionKit into Mobilize. For more information on how to set up your ActionKit integration with MobilizeAmerica, reach out to support@mobilizeamerica.io. 

New/Mode Campaign Engagement
*******************************

.. admonition:: vendor-managed integration

   `New/Mode <https://www.newmode.net/>`_ is a purpose-driven enterprise, providing sophisticated civic engagement tools to the world’s most important causes. They are campaigners, building what modern campaigns need to empower people, shape public decisions, and win. 

   With New/Mode's Advanced Engagement Tools you can extend ActionKit's already powerful features with new jurisdictions and action types, including:

   - Automated Letters to the Editor, backed by a complete database of newspapers in the US, Canada, UK and Australia
   - Tweet @YourRep (US, Canada, UK, Australia)
   - One-Click Call Your Representative (US, Canada, UK, Australia)
   - One-Click Email Your Representative (US, Canada, UK, Australia)
   - One-Click Fax Your Representative (US, Canada, UK, Australia)

   New/Mode action forms can be embedded in any website Content Management System and sync back to your ActionKit database.

   Contact Paul Stewart (paul@newmode.net) to learn more.

ThruText (previously Relay)
*******************************

.. admonition:: vendor-managed integration

   `ThruText <https://www.getthru.io/p2p-texting-nonprofits>`_ is a messaging platform that lets progressive organizations harness the power of peer-to-peer texting turn real conversations into action. 

   Learn more here: `https://help.getthru.io/support/solutions/articles/44001063886-actionkit-integration-event-rsvps <https://help.getthru.io/support/solutions/articles/44001063886-actionkit-integration-event-rsvps>`_.

ShareProgress
****************

.. admonition:: vendor-managed integration

   `Share Progress <http://www.shareprogress.org/>`_ provides sharing tools and share optimization for progressive organizations. You can use ShareProgress hosted share pages or share buttons on your own site in order to promote FaceBook, email, Twitter and click-to-copy sharing, and then easily A/B test variations on your share language and images. Analytics from the sharing can be passed through to your ActionKit database.

   * `Redirect to ShareProgress on ActionKit <http://support.shareprogress.org/knowledge_base/topics/how-do-i-redirect-share-pages-on-actionkit>`_

   * `Integrate analytics with ActionKit <http://support.shareprogress.org/knowledge_base/topics/how-can-i-integrate-shareprogress-analytics-with-actionkit>`_

Upland Mobile Commons
***********************

.. admonition:: vendor-managed integration

   The Upland Mobile Commons platform can be used to create personalized mobile messaging campaigns at scale. Using the  two-way data sync between the Upland Mobile Commons platform and ActionKit, you can grow your email and SMS lists while enabling efficient data completion.  To learn more, `request a demo <https://uplandsoftware.com/mobile-messaging/demo-request/>`_.

Publicly Available Queries, Code And Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://github.com/search?q=actionkit - Open source code in various languages with many functions.

https://www.drupal.org/node/2131947 -  Code to allow for creation and use of ActionKit petition pages and donation pages on a Drupal site.

https://github.com/MoveOnOrg/shopify-ak-import - Code to import shopify orders into ActionKit.
