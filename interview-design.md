### Interview design implementation Payments System

1. We need to create a tables business, payment
2. We need  to create a POST to request a new payment POST businesses/:id/payments/request -> Partial<Payment>
  We return the payment request of the business with a payment ID.
  The body contains the order_id, the amount, the accepted_payment_types (optional), expires_at (optional), user_id (in the JWT optional, jwt for now is not required)
3. Make a POST so a user can make a payment using the payment request ID and in the body it will have the payment information.
 POST /businesses/:id/payments/:id
 {
    amount,
    order_id, 
    payment_type,
    payment_information: { credit card number, name, etc}
    ..
 }
 4. Get all payments paginated by status and cursor descending order by created at
 