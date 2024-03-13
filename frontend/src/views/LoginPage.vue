<template>
    <NavBar />
    <div class="login">
        <form @submit.prevent="login">
            <h1>Login</h1>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" v-model="email" required />
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required />
            </div>
            <button type = "submit" class="btn btn-primary">Login</button> 
        </form>
    </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
export default{
    data(){
        return{
            email: '',
            password: ''
        };
    },
    methods:{
        async login(){
            try {
                const response = await fetch('http://localhost:5000/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password,
                    }),
                });
                const data = await response.json();
                console.log(data);
                if(response.ok){
                    alert(data.message);
                    localStorage.setItem("access_token", data.access_token);
                    this.$router.push('/');                }
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