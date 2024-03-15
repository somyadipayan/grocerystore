<template>
    <div class="container mt-5">
      <div v-if="loading">
        <h2>Loading...</h2>
      </div>
      <div v-else>
        <div v-if="product">
          <div class="card">
            <div class="card-header">
              <h2>{{ product.name }}</h2>
            </div>
            <div class="card-body">
              <dl class="row">
                <dt class="col-sm-3">Price:</dt>
                <dd class="col-sm-9">Rs.{{ product.rateperunit }}/{{ product.unit }}</dd>
  
                <dt class="col-sm-3">Quantity:</dt>
                <dd class="col-sm-9">{{ product.quantity }}</dd>
  
                <dt class="col-sm-3">Category:</dt>
                <dd class="col-sm-9">{{ product.category_name }}</dd>
              </dl>
              <div class="mt-4">
                <button v-if="role == 'user'" @click="orderProduct" class="btn btn-outline-success">Order</button>
                <button v-if="authorized" @click="updateProduct" class="btn btn-outline-primary">Update</button>
                <button v-if="authorized" @click="deleteProduct" class="btn btn-outline-danger">Delete</button>
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <p>No product found.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import userMixins from '../mixins/userMixins'
  
  export default {
    mixins: [userMixin],
    data() {
      return {
        product: null,
        loading: true,
      };
    },
    mounted() {
      this.fetchProductDetails();
    },
    methods: {
      fetchProductDetails() {
        const productId = this.$route.params.productId; 
        const token = localStorage.getItem('access_token');
  
        if (!token) {
          console.error('Access token is null');
          return;
        }
  
        fetch(`http://127.0.0.1:5000/product/${productId}`, {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
          },
        })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            this.product = data.product;
          })
          .catch(error => {
            console.error('Error fetching product details:', error);
          })
          .finally(() => {
            this.loading = false;
          });
      },
      orderProduct() {
        console.log('Order button clicked');
      },
      updateProduct() {
        this.$router.push(`/update-product/${this.product.id}`);
      },
      deleteProduct() {
        fetch(`http://127.0.0.1:5000/product/${this.product.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json',
          },
        })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            console.log(data.message);
            alert(data.message)
            this.$router.push('/');
          })
          .catch(error => {
            console.error('Error deleting product:', error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  .card {
    margin-top: 20px;
  }
  .btn {
    margin-right: 8px;
  }
  </style>
  