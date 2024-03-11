<template>
    <div class="register">
        <form @submit.prevent="register">
            <h1>Register</h1>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" v-model="email" required />
            </div>
            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" class="form-control" id="name" v-model="name" required />
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required />
            </div>
            <div class="mb-3">
                <label class="form-check-label" for="isManager">Register as manager</label>
                <input type="checkbox" class="form-check-input" id="isManager" v-model="isManager" />
            </div>
            <button type = "submit" class="btn btn-primary">Register</button> 
        </form>
    </div>
</template>

<script>
export default{
    data(){
        return{
            email: '',
            name: '',
            isManager: false,
            password: ''
        };
    },
    methods:{
        async register(){
            try {
                const response = await fetch('http://localhost:5000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        name: this.name,
                        password: this.password,
                        role: this.isManager ? 'manager' : 'user',
                    }),
                });
                const data = await response.json();
                console.log(data);
                if(response.ok){
                    alert(data.message);
                }
                else{
                    alert(data.error);
                }
            } catch (error) {
                console.log(error);
                alert("some error occured")
            }
            }
        }
    };
</script>

<style scoped>

</style>