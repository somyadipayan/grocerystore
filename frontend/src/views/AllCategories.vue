<template>
    <NavBar />
    <div class="container mt-5">
      <h2>Categories</h2>
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="category in categories" :key="category.id">
            <td>{{ category.id }}</td>
            <td>{{ category.name }}</td>
            <td>
              <div class="btn-group" role="group">
                <button v-if="this.role == 'admin'" class="btn btn-outline-primary" @click="updateCategory(category.id)">Update</button>
                <button v-if="this.role == 'admin'" class="btn btn-outline-danger" @click="deleteCategory(category.id)">Delete</button>
                <router-link v-if="this.role == 'admin' || this.role=='manager'" to="#">
                  <button class="btn btn-outline-success">Add Product</button>
                </router-link>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>

  <script>
  import userMixins from '../mixins/userMixins'
  import NavBar from '../components/NavBar.vue'
  export default{
    mixins: [userMixins],
    data(){
        return{
            categories: [],
        };
    },
    mounted() {
        this.getCategories();
    },
    methods: {
        getCategories() {
            fetch('http://127.0.0.1:5000/categories', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                this.categories = data.categories;
            })
            .catch(error => {
                console.error('Error:', error);
            })
        },
    updateCategory(categoryId) {
      this.$router.push({ name: 'UpdateCategory', params: { id: categoryId } });
    },
    deleteCategory(categoryId) {
      fetch(`http://127.0.0.1:5000/category/${categoryId}`, {
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
          console.log(`Category with ID ${categoryId} deleted successfully`);
          this.getCategories();
        })
        .catch(error => {
          console.error(`Error deleting category with ID ${categoryId}:`, error);
        });
    },
    }
  }
  </script>