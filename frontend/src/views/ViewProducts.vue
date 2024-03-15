<template>
    <div class="container mt-5">
      <h2>Products</h2>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Unit</th>
            <th>Rate per Unit</th>
            <th>Quantity</th>
            <!-- Add additional columns as needed -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.unit }}</td>
            <td>{{ product.rateperunit }}</td>
            <td>{{ product.quantity }}</td>
            <!-- Add additional cells as needed -->
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        products: [],
      };
    },
    mounted() {
      this.fetchProducts();
    },
    methods: {
      fetchProducts() {
        if (this.role === 'admin') {
          this.fetchAllProducts();
        } else if (this.role === 'manager') {
          this.fetchManagerProducts();
        }
      },
      fetchAllProducts() {
        fetch('http://localhost:5000/products', {
          method: 'GET',
        })
          .then(response => response.json())
          .then(data => {
            this.products = data.products;
          })
          .catch(error => {
            console.error('Error fetching all products:', error);
          });
      },
      fetchManagerProducts() {
        fetch('http://localhost:5000/products/my-products', {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          },
        })
          .then(response => response.json())
          .then(data => {
            this.products = data.user_products;
          })
          .catch(error => {
            console.error('Error fetching your products:', error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your custom styles here */
  </style>
  