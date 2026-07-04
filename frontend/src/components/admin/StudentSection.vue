<template>
  <div class="row my-3">
    <div class="col-12">
      <div class="card shadow h-100">
        <div class="card-body">
          <h3 class="card-title">Students</h3>
          <div class="mt-4">
            <h4 class="text-muted">Approved Students</h4>
            <div class="table-responsive" v-if="dashboard.approvedStudents.length !== 0">
              <table class="table text-center">
                <thead>
                  <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                  <tr v-for="student in dashboard.approvedStudents" :key="student.user_id">
                    <td>{{ student.user_id }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ student.email }}</td>
                    <td><button class="btn btn-danger" @click="$emit('blacklistStudent', student.user_id)">Blacklist</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p
              class="text-center fw-bold text-secondary my-3"
              v-if="dashboard.approvedStudents.length === 0"
            >
              No approved students
            </p>
          </div>
          <div class="mt-4">
            <h4 class="text-muted">Blacklisted Students</h4>
            <div class="table-responsive" v-if="dashboard.removedStudents.length !== 0">
              <table class="table text-center">
                <thead>
                  <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                  </tr>
                </thead>
                <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                  <tr v-for="student in dashboard.removedStudents" :key="student.user_id">
                    <td>{{ student.user_id }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ student.email }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p
              class="text-center fw-bold text-secondary my-3"
              v-if="dashboard.removedStudents.length === 0"
            >
              No blacklisted students
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
