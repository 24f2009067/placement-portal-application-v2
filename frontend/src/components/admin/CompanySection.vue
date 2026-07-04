<template>
  <div class="row my-3">
    <div class="col-12">
      <div class="card shadow h-100">
        <div class="card-body">
          <h3 class="card-title">Companies</h3>

          <div class="mt-4">
            <h4 class="text-muted">Pending Companies</h4>
            <div class="table-responsive" v-if="dashboard.pendingCompanies.length !== 0">
              <table class="table text-center">
                <thead>
                  <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Industry</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                  <tr v-for="company in dashboard.pendingCompanies" :key="company.user_id">
                    <td>{{ company.user_id }}</td>
                    <td>{{ company.name }}</td>
                    <td>{{ company.email }}</td>
                    <td>{{ company.industry }}</td>
                    <td>
                      <button
                        class="btn btn-success"
                        @click="$emit('approveCompany', company.user_id)"
                      >
                        Approve
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p
              class="text-center fw-bold text-secondary my-3"
              v-if="dashboard.pendingCompanies.length === 0"
            >
              No pending company approvals
            </p>
          </div>

          <div class="mt-4">
            <h4 class="text-muted">Approved Companies</h4>
            <div class="table-responsive" v-if="dashboard.approvedCompanies.length !== 0">
              <table class="table text-center">
                <thead>
                  <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Industry</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                  <tr v-for="company in dashboard.approvedCompanies" :key="company.user_id">
                    <td>{{ company.user_id }}</td>
                    <td>{{ company.name }}</td>
                    <td>{{ company.email }}</td>
                    <td>{{ company.industry }}</td>
                    <td>
                      <button
                        class="btn btn-danger"
                        @click="$emit('blacklistCompany', company.user_id)"
                      >
                        Blacklist
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p
              class="text-center fw-bold text-secondary my-3"
              v-if="dashboard.approvedCompanies.length === 0"
            >
              No approved companies
            </p>
          </div>

          <div class="mt-4">
            <h4 class="text-muted">Blacklisted Companies</h4>
            <div class="table-responsive" v-if="dashboard.removedCompanies.length !== 0">
              <table class="table text-center">
                <thead>
                  <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Industry</th>
                  </tr>
                </thead>
                <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                  <tr v-for="company in dashboard.removedCompanies" :key="company.user_id">
                    <td>{{ company.user_id }}</td>
                    <td>{{ company.name }}</td>
                    <td>{{ company.email }}</td>
                    <td>{{ company.industry }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p
              class="text-center fw-bold text-secondary my-3"
              v-if="dashboard.removedCompanies.length === 0"
            >
              No blacklisted companies
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
defineProps(['dashboard'])
</script>
