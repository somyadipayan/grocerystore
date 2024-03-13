<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/">Shopper's Stop</router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
                aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav">
                    <li v-if="!this.loggedin" class="nav-item">
                        <router-link class="nav-link" to="/login">Login</router-link>
                    </li>
                    <li v-if="!this.loggedin" class="nav-item">
                        <a class="nav-link" href="#">Register</a>
                    </li>
                    <li v-if="this.loggedin" class="nav-item">
                        <a class="nav-link" href="#">Create Category</a>
                    </li>
                    <li  v-if="this.loggedin && (this.role=='admin')" class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            Admin Actions
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#">Manager Applications</a></li>
                            <li><a class="dropdown-item" href="#">Create category</a></li>
                        </ul>
                    </li>
                    <li v-if="this.loggedin" class="nav-item">
                        <a @click="logout" class="nav-link">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
<script>
import userMixins from '../mixins/userMixins'
export default {
    mixins: [userMixins]
}

</script>
