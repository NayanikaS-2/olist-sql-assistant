\# Olist E-commerce Data Dictionary



Brazilian online marketplace data, 2016-2018. Money is in Brazilian reais (BRL).



\## orders (one row per order)

\- order\_id: unique order ID (primary key)

\- customer\_id: links to customers.customer\_id (one per order)

\- order\_status: delivered, shipped, canceled, unavailable, invoiced, processing, created, approved

\- order\_purchase\_timestamp: when the customer placed the order

\- order\_approved\_at: when payment was approved

\- order\_delivered\_carrier\_date: when the order was handed to the carrier

\- order\_delivered\_customer\_date: when the customer actually received it

\- order\_estimated\_delivery\_date: delivery date promised to the customer



\## customers (one row per customer\_id)

\- customer\_id: links to orders.customer\_id (changes with every order)

\- customer\_unique\_id: identifies the real person across multiple orders

\- customer\_zip\_code\_prefix: first 5 digits of the zip code

\- customer\_city, customer\_state: location (state is a 2-letter code like SP)



\## order\_items (one row per item in an order)

\- order\_id: links to orders.order\_id

\- order\_item\_id: item number within the order (1, 2, 3...)

\- product\_id: links to products.product\_id

\- seller\_id: links to sellers.seller\_id

\- shipping\_limit\_date: deadline for the seller to hand to the carrier

\- price: item price in BRL

\- freight\_value: shipping cost for the item in BRL



\## order\_payments (one row per payment on an order)

\- order\_id: links to orders.order\_id

\- payment\_sequential: payment number if split across methods

\- payment\_type: credit\_card, boleto, voucher, debit\_card

\- payment\_installments: number of installments chosen

\- payment\_value: amount paid in BRL



\## order\_reviews (customer reviews)

\- review\_id: unique review ID

\- order\_id: links to orders.order\_id

\- review\_score: 1 (worst) to 5 (best)

\- review\_comment\_title, review\_comment\_message: free text in Portuguese

\- review\_creation\_date, review\_answer\_timestamp: review dates



\## products

\- product\_id: unique product ID

\- product\_category\_name: category in Portuguese (join to translation table for English)

\- product\_name\_lenght, product\_description\_lenght: text lengths (spelled "lenght" in the data)

\- product\_photos\_qty: number of photos

\- product\_weight\_g, product\_length\_cm, product\_height\_cm, product\_width\_cm: size and weight



\## sellers

\- seller\_id: unique seller ID

\- seller\_zip\_code\_prefix, seller\_city, seller\_state: seller location



\## product\_category\_name\_translation

\- product\_category\_name: Portuguese category name

\- product\_category\_name\_english: English category name



\## geolocation

\- Zip code prefixes with latitude and longitude. Rarely needed.



\## How the tables connect

orders.customer\_id -> customers.customer\_id

order\_items.order\_id -> orders.order\_id

order\_items.product\_id -> products.product\_id

order\_items.seller\_id -> sellers.seller\_id

order\_payments.order\_id -> orders.order\_id

order\_reviews.order\_id -> orders.order\_id

products.product\_category\_name -> product\_category\_name\_translation.product\_category\_name



\## Conventions

\- When asked about orders or revenue "by month" or "per month" without saying which date, group by order\_purchase\_timestamp (the purchase date), not the delivery date.

