<template>
    <div style="padding: 5%;">
      <h2>Manager Applications</h2>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Name</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="manager in managerApplications" :key="manager.id">
            <td>{{ manager.id }}</td>
            <td>{{ manager.email }}</td>
            <td>{{ manager.name }}</td>
            <td>{{ manager.role }}</td>
            <td>
              <button class="btn btn-primary" @click="verifyManager(manager.id, true)">
                Verify
              </button>
              <button class="btn btn-danger" @click="verifyManager(manager.id, false)">
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>

  <script>
export default{
    data() {
        return {
        managerApplications: []
        };
    },
    mounted(){
        this.getManagerApplications();
    },
    methods: {
        getManagerApplications() {
            const token = localStorage.getItem("access_token");
            console.log(token);
            fetch("http://127.0.0.1:5000/manager-applications",{
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem("access_token"),
                },
            })
            .then(response => {
                console.log(response);
                if(!response.ok){
                    throw new Error(`HTTP error: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                this.managerApplications = data.manager_applications;
            })
            .catch(error => {
                console.log(error);
            });
        },
        verifyManager(managerId, isVerify) {
            const action = isVerify ? 'veridfy' : 'reject';
            console.log(`Manager ${managerId} ${action}`);
            const menthod = isVerify ? 'PUT' : 'DELETE';
            fetch('http://127.0.0.1:5000/manager-approve/' + managerId, {
                method: menthod,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem("access_token"),
                },
            })
            .then(response => {
                if(!response.ok){
                    throw new Error(`HTTP error: ${response.status}`);
                }
                console.log(`Success: Manager ${managerId} ${action}`)
                alert('success')
                this.getManagerApplications();
            })
            .catch(error => {
                console.log(error);
            });
        }
    }
}


</script>

