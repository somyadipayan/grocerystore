<template>
    <div class="container mt-5">
      <div class="card">
        <div class="card-header">
          <h2>Add Product</h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="addProduct" class="row g-3">
            <div class="col-md-6">
              <label for="productName" class="form-label">Product Name:</label>
              <input v-model="productName" type="text" class="form-control" id="productName" required />
            </div>
            <div class="col-md-6">
              <label for="productUnit" class="form-label">Unit:</label>
              <input v-model="productUnit" type="text" class="form-control" id="productUnit" required />
            </div>
            <div class="col-md-6">
              <label for="productRate" class="form-label">Rate per Unit:</label>
              <input v-model="productRate" type="number" class="form-control" id="productRate" required />
            </div>
            <div class="col-md-6">
              <label for="productQuantity" class="form-label">Quantity:</label>
              <input v-model="productQuantity" type="number" class="form-control" id="productQuantity" required />
            </div>
            <div class="col-md-6">
                <label for="categoryDropdown" class="form-label">Category:</label>
                <select v-model="selectedCategory" class="form-select" id="categoryDropdown" required>
                <option disabled value="">Select Category</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
                </select>
            </div>
            <div class="col-12 mt-3">
              <button type="submit" class="btn btn-primary">Add Product</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
export default {
  data() {
    return {
      productName: '',
      productUnit: '',
      productRate: null,
      productQuantity: null,
      selectedCategory: null,
      categories: [],
    };
  },
  created() {
    this.fetchCategories();
    const categoryIdFromRoute = this.$route.params.id;
    console.log(categoryIdFromRoute)
    if (categoryIdFromRoute) {
      this.selectedCategory = categoryIdFromRoute;
      console.log(this.selectedCategory);
    }
  },
  methods: {
    fetchCategories() {
      fetch('http://127.0.0.1:5000/categories', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
        .then(response => response.json())
        .then(data => {
          this.categories = data.categories;
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
        });
    },
    addProduct() {
      fetch(`http://127.0.0.1:5000/category/${this.selectedCategory}/add-product`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
        body: JSON.stringify({
          name: this.productName,
          unit: this.productUnit,
          rateperunit: this.productRate,
          quantity: this.productQuantity,
        }),
      })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          this.$router.push('/');
          // Optionally, you can redirect or perform other actions after adding the product
        })
        .catch(error => {
          console.error('Error adding product:', error);
        });
    },
  },
};
</script>

  
  <style>
  /* Add your custom styles here */
  </style>
  