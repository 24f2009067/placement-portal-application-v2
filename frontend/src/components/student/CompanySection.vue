<template>
  <div class="row my-3">
    <div class="col-12">
      <div class="card shadow h-100">
        <div class="card-body">
          <h3 class="card-title">Companies</h3>
          <div class="mt-4">
            <div class="table-responsive" v-if="dashboard.companies.length !== 0">
              <table class="table text-center">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Industry</th>
                    <th>Location</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                  <tr v-for="company in dashboard.companies" :key="company.user_id">
                    <td><a :href="company.website" target="blank">{{ company.name }}</a></td>
                    <td>{{ company.email }}</td>
                    <td>{{ company.industry }}</td>
                    <td>{{ company.location }}</td>
                    <td><button class="btn btn-dark" @click="viewCompany(company.user_id)">View</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p
              class="text-center fw-bold text-secondary my-3"
              v-if="dashboard.companies.length === 0"
            >
              No companies
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { useRouter } from 'vue-router';

defineProps(['dashboard'])
const router = useRouter()

function viewCompany(user_id){
  router.push({name: "companyDetails", params: {id: user_id}})
}
</script>
