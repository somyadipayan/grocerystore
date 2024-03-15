<template>
  <NavBar />
  <div class="container mt-5">
    <h2 v-if="user" class="mb-4">Hello, {{user.name}}</h2>
    <h2 v-else class="mb-4">Please Login to Shop</h2>
    <div class="mb-4">
      <label for="searchInput" class="me-2">Search Product:</label>
      <input v-model="searchQuery" type="text" id="searchInput" class="form-control" @input="searchProducts" placeholder="Type to search..." />
    </div>
    <div v-for="category in categories" :key="category.id">
      <div v-if="category.visible !== false && category.products.length !== 0">
        <h2>{{ category.name }} <router-link :to="`/add-products/${category.id}`">Add Product</router-link></h2>
        <div class="row">
          <div v-for="product in category.products" :key="product.id" class="col-md-4 mb-4">
            <div v-if="product.visible !== false" class="card">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h4>{{ product.name }}</h4>
                <router-link v-if="role=='admin' || role=='manager'" :to="'/view-product/' + product.id">view product</router-link>
              </div>
              <div class="card-body">
                <dl class="row">
                  <dt class="col-sm-4">Price:</dt>
                  <dd class="col-sm-8">Rs.{{ product.rateperunit }}/{{ product.unit }}</dd>

                  <dt class="col-sm-4">Stock Left:</dt>
                  <dd v-if="product.quantity!=0" class="col-sm-8">{{ product.quantity }}</dd>
                  <dd v-else class="col-sm-8">SOLD OUT</dd>

                  <dt class="col-sm-4">Category:</dt>
                  <dd class="col-sm-8">{{ category.name }}</dd>
                </dl>
                <div v-if="user" class="mb-3 d-flex align-items-center">
                  <label for="quantityInput" class="me-2">Quantity:</label>
                  <input v-model="product.quantityInput" type="number" id="quantityInput" class="form-control"
                  style="max-width: 15%;" pattern="[1-9]\d*" title="Please enter a positive integer (non-zero)" />
                  <button v-if="product.quantity!=0" @click="addToCart(product)" class="btn btn-success ms-2">Add to Cart</button>
                  <button v-else class="btn btn-secondary ms-2" disabled>Add to Cart</button>

                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import UserMixins from '../mixins/userMixins';
export default {
  mixins: [UserMixins],
  data() {
    return {
      categories: [],
      searchQuery: ''
    };
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    fetchCategories() {
      fetch('http://127.0.0.1:5000/categories', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data)
          this.categories = data.categories.map((category) => ({
            id: category.id,
            name: category.name,
            products: [],
          }));

          this.fetchProductsForCategories();
        })
        .catch((error) => {
          console.error('Error fetching categories:', error);
        });
    },
    fetchProductsForCategories() {
      this.categories.forEach((category) => {
        fetch(`http://127.0.0.1:5000/category/${category.id}/products`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then((response) => response.json())
          .then((data) => {
            category.products = data.products.map((product) => ({
              ...product,
              visible: true,
            }));
          })
          .catch((error) => {
            console.error(`Error fetching products for category ${category.name}:`, error);
          });
      });
    },
    addToCart(product) {
      const productId = product.id;
      const quantity = product.quantityInput || 1;

      fetch(`http://127.0.0.1:5000/add-to-cart/${productId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
        body: JSON.stringify({ quantity }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Failed to add product to cart');
          }
          return response.json();
        })
        .then((data) => {
          console.log(data.message);
          alert(data.message);
          product.quantityInput = '';
        })
        .catch((error) => {
          alert(error.message || 'Error adding product to cart');
          console.error('Error adding product to cart:', error);
        });
    },
    searchProducts() {
      const query = this.searchQuery.toLowerCase();

      this.categories.forEach((category) => {
        let categoryVisible = false; 

        category.products.forEach((product) => {
          const productName = product.name.toLowerCase();
          if (productName.includes(query)) {
            product.visible = true;
            categoryVisible = true;
          } else {
            product.visible = false;
          }
        });

        category.visible = categoryVisible;
      });
    },
  },
};
</script>

<style scoped>
.card {
  margin-top: 20px;
}
.float{
	position:fixed;
	width:60px;
	height:60px;
	bottom:70px;
	right:70px;
	background-color:#0C9;
	color:#FFF;
	border-radius:50px;
	text-align:center;
	box-shadow: 2px 2px 3px #999;
}

.my-float{
	margin-top:15px;
}
</style>
