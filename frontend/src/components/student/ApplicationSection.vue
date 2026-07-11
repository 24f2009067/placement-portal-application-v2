<template>
  <div class="row my-3">
    <div class="col-12">
      <div class="card shadow h-100">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center flex-wrap">
            <h3 class="card-title">Applications</h3>
            <button class="btn btn-info text-nowrap" @click="handleGenerateReport">Generate Report</button>
          </div>
          <div class="table-responsive" v-if="dashboard.applications.length !== 0">
            <table class="table text-center">
              <thead>
                <tr>
                  <th>Application ID</th>
                  <th>Company Name</th>
                  <th>Job Position</th>
                  <th>Status</th>
                  <th>Date</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                <tr v-for="application in dashboard.applications" :key="application.application_id">
                  <td>{{ application.application_id }}</td>
                  <td>{{ application.company_name }}</td>
                  <td>{{ application.job_title }}</td>
                  <td>{{ application.status }}</td>
                  <td>{{ new Date(application.created_on).toLocaleString() }}</td>
                  <td>
                    <button
                      class="btn btn-dark"
                      @click="$emit('getApplication', application.application_id)"
                    >
                      view
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p
            class="text-center fw-bold text-secondary my-3"
            v-if="dashboard.applications.length === 0"
          >
            No applications
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { generateReport } from '@/api/student';
import { showToast } from '@/toast';

defineProps(['dashboard'])

async function handleGenerateReport() {
  const data = await generateReport()
  if (data) {
    showToast("Student Dashboard", "The report will be mailed to you shortly.")
  }
}
</script>
