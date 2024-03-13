<template>
    <div class="container mt-5">
      <h2>Update Category</h2>
      <form @submit.prevent="updateCategory" class="mt-3">
        <div class="mb-3">
          <label for="name" class="form-label">Category Name:</label>
          <input v-model="categoryName" type="text" id="name" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary">Update Category</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        categoryName: '',
      };
    },
    mounted() {
      const categoryId = this.$route.params.id;
      this.fetchCategoryDetails(categoryId);
    },
    methods: {
      fetchCategoryDetails(categoryId) {
        const token = localStorage.getItem('access_token');
  
        if (!token) {
          console.error('Access token is null');
          return;
        }
  
        fetch(`http://127.0.0.1:5000/category/${categoryId}`, {
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
            this.categoryName = data.category_data.name;
          })
          .catch(error => {
            console.error(`Error fetching category details for ID ${categoryId}:`, error);
          });
      },
      updateCategory() {
        const token = localStorage.getItem('access_token');
  
        if (!token) {
          console.error('Access token is null');
          return;
        }
  
        const categoryId = this.$route.params.id;
  
        fetch(`http://127.0.0.1:5000/category/${categoryId}`, {
          method: 'PUT',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.categoryName,
          }),
        })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log(`Category with ID ${categoryId} updated successfully`);
            this.$router.push({ name: 'allcategories' });
          })
          .catch(error => {
            console.error(`Error updating category with ID ${categoryId}:`, error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your custom styles here */
  </style>
  