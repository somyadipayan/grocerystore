export default{
    data(){
        return{
            user: null,
            role: null,
            loggedin: false
        };
    },
    async created(){
        await this.checkauth();
    },
    methods:
{
    async checkauth(){
        const accessToken = localStorage.getItem('access_token');
        if(!accessToken){
            this.loggedin = false;
            return
        }
        try{
            this.user = await this.getuserinfo(accessToken);
            this.role = this.user.role;
        } catch (error) {
            console.log("Error Fetching user info", error);
            this.loggedin = false;
        }
    },
    async getuserinfo(accessToken){
        const response = await fetch('http://localhost:5000/getuserinfo', {
            methods: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        });
        if(!response.ok){   // 401, 404
            this.loggedin = false;
            return null;
        }
        this.loggedin = true;
        return await response.json();
    },
    async logout(){
        fetch('http://localhost:5000/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        .then(() => {
            localStorage.removeItem('access_token');
            this.user = null;
            this.$router.push('/login')
        })
        .catch(error => {
            console.log("Error logging out", error);
        })
    }
}
    }