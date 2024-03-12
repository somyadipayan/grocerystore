<template>
    <div class="container mt-5">
      <h2>Create Category</h2>
      <form @submit.prevent="createCategory" class="mt-3">
        <div class="mb-3">
          <label for="categoryName" class="form-label">Category Name</label>
          <input v-model="categoryName" type="text" class="form-control" id="categoryName" required>
        </div>
        <button type="submit" class="btn btn-primary">Create Category</button>
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
    methods: {
      async createCategory() {
        try {
          const response = await fetch('http://localhost:5000/category', {
            method: 'POST',
            headers: {
              'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              name: this.categoryName,
            }),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            alert(data.message);
            //this.$routerKey.push('/all-categories');
            // Route to all categories
          } else {
            alert('Error: ' + data.error);
          }
        } catch (error) {
          console.error('Create category error:', error);
          alert('An error occurred while creating the category.');
        }
      },
    },
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  