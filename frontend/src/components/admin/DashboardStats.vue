<template>
  <div class="row g-3">
    <div class="col-12 col-xl-4">
      <div class="card shadow h-100">
        <div class="card-body">
          <h3 class="text-center mb-4">Students</h3>
          <div class="row">
            <div class="col">
              <div class="text-center" style="min-height: 3rem">Total</div>
              <div class="text-center fw-bold text-light">{{ totalStudents }}</div>
            </div>
            <div class="col">
              <div class="text-center" style="min-height: 3rem">Active</div>
              <div class="text-center fw-bold text-success">
                {{ dashboard.approvedStudents.length }}
              </div>
            </div>
            <div class="col">
              <div class="text-center" style="min-height: 3rem">Blacklisted</div>
              <div class="text-center fw-bold text-danger">
                {{ dashboard.removedStudents.length }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="col-12 col-xl-4">
      <div class="card h-100 shadow">
        <div class="card-body">
          <h3 class="text-center mb-4">Company</h3>
          <div class="row">
            <div class="col">
              <div class="text-center" style="min-height: 3rem">Total</div>
              <div class="text-center fw-bold text-light">{{ totalCompanies }}</div>
            </div>
            <div class="col">
              <div class="text-center" style="min-height: 3rem">Active</div>
              <div class="text-center text-success fw-bold">
                {{ dashboard.approvedCompanies.length }}
              </div>
            </div>
            <div class="col">
              <div class="text-center" style="min-height: 3rem">Blacklisted</div>
              <div class="text-center text-danger fw-bold">
                {{ dashboard.removedCompanies.length }}
              </div>
            </div>
            <div class="col">
              <div class="text-center" style="min-height: 3rem">Pending</div>
              <div class="text-center text-warning fw-bold">
                {{ dashboard.pendingCompanies.length }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="col-12 col-xl-4">
      <div class="card shadow">
        <div class="card-body">
          <h3 class="text-center mb-4">Drives</h3>
          <div class="row">
            <div class="col">
              <div class="text-center" style="min-height: 3rem">Total</div>
              <div class="text-center fw-bold text-light">{{ totalDrives }}</div>
            </div>
            <div class="col">
              <div class="text-center" style="min-height: 3rem">Active</div>
              <div class="text-center text-success fw-bold">
                {{ dashboard.approvedDrives.length }}
              </div>
            </div>
            <div class="col">
              <div class="text-center" style="min-height: 3rem">Closed / Blacklisted</div>
              <div class="text-center text-danger fw-bold">
                {{ dashboard.closedDrives.length + dashboard.removedDrives.length }}
              </div>
            </div>
            <div class="col">
              <div class="text-center" style="min-height: 3rem">Pending</div>
              <div class="text-center text-warning fw-bold">
                {{ dashboard.pendingDrives.length }}
              </div>
            </div>
          </div>
        </div>
        <div class="text-bg-warning">
          <div class="text-center fw-bold text-black">
            {{ dashboard.applications.length }} applications
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from 'vue'

const props = defineProps(['dashboard'])

const totalCompanies = computed(() => {
  return (
    props.dashboard.removedCompanies.length +
    props.dashboard.approvedCompanies.length +
    props.dashboard.pendingCompanies.length
  )
})

const totalDrives = computed(() => {
  return (
    props.dashboard.pendingDrives.length +
    props.dashboard.approvedDrives.length +
    props.dashboard.closedDrives.length +
    props.dashboard.removedDrives.length
  )
})

const totalStudents = computed(() => {
  return props.dashboard.approvedStudents.length + props.dashboard.removedStudents.length
})
</script>
