<template>
  <div class="row my-3">
    <div class="col-12">
      <div class="card shadow h-100">
        <div class="card-body">
          <h3 class="card-title">Drives</h3>

          <div class="mt-4">
            <h4 class="text-muted">Pending Drives</h4>
            <div class="table-responsive" v-if="dashboard.pendingDrives.length !== 0">
              <table class="table text-center">
                <thead>
                  <tr>
                    <th>Drive ID</th>
                    <th>Company Name</th>
                    <th>Job Position</th>
                    <th>Deadline</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                  <tr v-for="drive in dashboard.pendingDrives" :key="drive.drive_id">
                    <th>{{ drive.drive_id }}</th>
                    <th>{{ drive.company_name }}</th>
                    <th>{{ drive.job_title }}</th>
                    <th>{{ drive.deadline }}</th>
                    <th><button class="btn btn-success" @click="$emit('approveDrive', drive.drive_id)">Approve</button></th>
                  </tr>
                </tbody>
              </table>
            </div>
            <p
              class="text-center fw-bold text-secondary my-3"
              v-if="dashboard.pendingDrives.length === 0"
            >
              No pending drive approvals
            </p>
          </div>

          <div class="mt-4">
            <h4 class="text-muted">Approved Drives</h4>
            <div class="table-responsive" v-if="dashboard.approvedDrives.length !== 0">
              <table class="table text-center">
                <thead>
                  <tr>
                    <th>Drive ID</th>
                    <th>Company Name</th>
                    <th>Job Position</th>
                    <th>Deadline</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                  <tr v-for="drive in dashboard.approvedDrives" :key="drive.drive_id">
                    <th>{{ drive.drive_id }}</th>
                    <th>{{ drive.company_name }}</th>
                    <th>{{ drive.job_title }}</th>
                    <th>{{ drive.deadline }}</th>
                    <th>
                      <div class="d-flex justify-content-center align-content-center">
                        <button class="btn btn-dark mx-1" @click="$emit('getDrive', drive.drive_id)">view</button>
                        <button class="btn btn-success mx-1 text-nowrap" @click="$emit('closeDrive', drive.drive_id)">mark as closed</button>
                        <button class="btn btn-danger mx-1" @click="$emit('blacklistDrive', drive.drive_id)">blacklist</button>
                      </div>
                    </th>
                  </tr>
                </tbody>
              </table>
            </div>
            <p
              class="text-center fw-bold text-secondary my-3"
              v-if="dashboard.approvedDrives.length === 0"
            >
              No approved drive
            </p>
          </div>

          <div class="mt-4">
            <h4 class="text-muted">Closed Drives</h4>
            <div class="table-responsive" v-if="dashboard.closedDrives.length !== 0">
              <table class="table text-center">
                <thead>
                  <tr>
                    <th>Drive ID</th>
                    <th>Company Name</th>
                    <th>Job Position</th>
                    <th>Deadline</th>
                  </tr>
                </thead>
                <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                  <tr v-for="drive in dashboard.closedDrives" :key="drive.drive_id">
                    <th>{{ drive.drive_id }}</th>
                    <th>{{ drive.company_name }}</th>
                    <th>{{ drive.job_title }}</th>
                    <th>{{ drive.deadline }}</th>
                  </tr>
                </tbody>
              </table>
            </div>
            <p
              class="text-center fw-bold text-secondary my-3"
              v-if="dashboard.closedDrives.length === 0"
            >
              No closed drive
            </p>
          </div>

          <div class="mt-4">
            <h4 class="text-muted">Blacklisted Drives</h4>
            <div class="table-responsive" v-if="dashboard.removedDrives.length !== 0">
              <table class="table text-center">
                <thead>
                  <tr>
                    <th>Drive ID</th>
                    <th>Company Name</th>
                    <th>Job Position</th>
                    <th>Deadline</th>
                  </tr>
                </thead>
                <tbody style="border-top: 0.1rem solid rgba(255, 255, 255, 0.2)">
                  <tr v-for="drive in dashboard.removedDrives" :key="drive.drive_id">
                    <th>{{ drive.drive_id }}</th>
                    <th>{{ drive.company_name }}</th>
                    <th>{{ drive.job_title }}</th>
                    <th>{{ drive.deadline }}</th>
                  </tr>
                </tbody>
              </table>
            </div>
            <p
              class="text-center fw-bold text-secondary my-3"
              v-if="dashboard.removedDrives.length === 0"
            >
              No blacklisted drive
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
