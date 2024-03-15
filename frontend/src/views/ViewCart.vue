<template>
    <div class="container mt-5">
      <h2>Your Shopping Cart</h2>
      <div v-if="cart">
        <div v-for="item in cart" :key="item.product_id" class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">{{ item.name }}</h5>
            <p class="card-text">
              <strong>Quantity:</strong>
              <input type="number" v-model="item.quantity" @change="updateCartItem(item)" style="max-width: 15%;"/>
              {{ item.unit }}(s)<br>
              <strong>Price per unit:</strong> Rs.{{ item.price_per_unit }}/{{ item.unit }}<br>
              <strong>Total Price:</strong> Rs.{{ item.total_price }}
            </p>
            <button @click="removeItemFromCart(item)" class="btn btn-danger">Remove</button>
          </div>
        </div>
        <div class="mt-3">
          <p><strong>Total Amount:</strong> Rs.{{ totalAmount }}</p>
          <button @click="placeOrder" class="btn btn-success">Place Order</button>
        </div>
      </div>
      <div v-else>
        <p>Your shopping cart is empty.</p>
      </div>
    </div>
  </template>
    
  <script>
  export default {
    data() {
      return {
        cart: [],
        totalAmount: 0,
      };
    },
    mounted() {
      this.viewCart();
    },
    methods: {
      viewCart() {
        fetch('http://127.0.0.1:5000/view-cart', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        })
          .then((response) => response.json())
          .then((data) => {
            this.cart = data.cart;
            this.calculateTotalAmount();
          })
          .catch((error) => {
            console.error('Error fetching cart:', error);
          });
      },
      calculateTotalAmount() {
        this.totalAmount = this.cart.reduce((total, item) => total + item.total_price, 0);
      },
      placeOrder() {
        fetch('http://127.0.0.1:5000/order', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.message) {
              console.log(data.message);
              alert(data.message);
            }
            if (data.error) {
              console.log(data.error);
              alert(data.error);
            }
            this.viewCart();
          })
          .catch((error) => {
            console.error('Error placing order:', error);
          });
      },
      updateCartItem(item) {
        fetch(`http://127.0.0.1:5000/update-cart/${item.product_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
          body: JSON.stringify({ quantity: item.quantity }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.message) {
              console.log(data.message);
              alert(data.message);
            }
            if (data.error) {
              console.log(data.error);
              alert(data.error);
            }
            this.viewCart();
          })
          .catch((error) => {
            console.error('Error updating cart item:', error);
          });
      },
      removeItemFromCart(item) {
        fetch(`http://127.0.0.1:5000/remove-from-cart/${item.product_id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.message) {
              console.log(data.message);
              alert(data.message);
            }
            if (data.error) {
              console.log(data.error);
              alert(data.error);
            }
            this.viewCart();
          })
          .catch((error) => {
            console.error('Error removing item from cart:', error);
          });
      },
    },
  };
  </script>
    
  <style scoped>
  .card {
    max-width: 400px;
    margin-bottom: 20px;
  }
  </style>
    