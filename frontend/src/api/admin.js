const API_URL = import.meta.env.VITE_API_URL
import { showToast } from '@/toast'
import { api } from './utility'

export async function loadDashboard(s) {
  try {
    const [
      approvedCompanies,
      removedCompanies,
      pendingCompanies,
      approvedStudents,
      removedStudents,
      applications,
      approvedDrives,
      pendingDrives,
      closedDrives,
      removedDrives,
    ] = await Promise.all([
      api(`${API_URL}/api/admin/companies?status=approved&search=${s}`),
      api(`${API_URL}/api/admin/companies?status=removed&search=${s}`),
      api(`${API_URL}/api/admin/companies?status=pending&search=${s}`),

      api(`${API_URL}/api/admin/students?status=approved&search=${s}`),
      api(`${API_URL}/api/admin/students?status=removed&search=${s}`),

      api(`${API_URL}/api/admin/applications?search=${s}`),

      api(`${API_URL}/api/admin/drives?status=approved&search=${s}`),
      api(`${API_URL}/api/admin/drives?status=pending&search=${s}`),
      api(`${API_URL}/api/admin/drives?status=closed&search=${s}`),
      api(`${API_URL}/api/admin/drives?status=removed&search=${s}`),
    ])

    return {
      approvedCompanies: approvedCompanies.companies,
      removedCompanies: removedCompanies.companies,
      pendingCompanies: pendingCompanies.companies,

      approvedStudents: approvedStudents.students,
      removedStudents: removedStudents.students,

      applications: applications.applications,

      approvedDrives: approvedDrives.drives,
      pendingDrives: pendingDrives.drives,
      closedDrives: closedDrives.drives,
      removedDrives: removedDrives.drives,
    }
  } catch (e) {
    showToast('Admin Dashboard', e.message || 'Something went wrong!')
  }
}

// company ---
// approval
export async function sendApproveCompany(user_id) {
  try {
    const data = await api(`${API_URL}/api/admin/companies/${user_id}/approve`, { method: 'PUT' })
    return data
    
  } catch (e) {
    showToast('Admin Dashboard', e.message || 'Something went wrong!')
  }
}

// blacklist
export async function sendBlacklistCompany(user_id) {
  try {
    const data = await api(`${API_URL}/api/admin/companies/${user_id}/remove`, { method: 'DELETE' })
    return data
    
  } catch (e) {
    showToast('Admin Dashboard', e.message || 'Something went wrong!')
  }
}

// students --
// blacklist
export async function sendBlacklistStudent(user_id) {
  try {
    const data = await api(`${API_URL}/api/admin/students/${user_id}/remove`, { method: 'DELETE' })
    return data
    
  } catch (e) {
    showToast('Admin Dashboard', e.message || 'Something went wrong!')
  }
}

// Drive ---
// blacklist
export async function sendBlacklistDrive(drive_id) {
  try {
    const data = await api(`${API_URL}/api/admin/drives/${drive_id}/remove`, { method: 'DELETE' })
    return data
    
  } catch (e) {
    showToast('Admin Dashboard', e.message || 'Something went wrong!')
  }
}

// approve
export async function sendApproveDrive(drive_id) {
  try {
    const data = await api(`${API_URL}/api/admin/drives/${drive_id}/approve`, { method: 'PUT' })
    return data
    
  } catch (e) {
    showToast('Admin Dashboard', e.message || 'Something went wrong!')
  }
}

// close
export async function sendCloseDrive(drive_id) {
  try {
    const data = await api(`${API_URL}/api/admin/drives/${drive_id}/close`, { method: 'PUT' })
    return data
    
  } catch (e) {
    showToast('Admin Dashboard', e.message || 'Something went wrong!')
  }
}


// card ---
export async function sendGetApplications(application_id) {
  try {
    const data = await api(`${API_URL}/api/admin/applications/${application_id}`)
    return data
    
  } catch (e) {
    showToast('Admin Dashboard', e.message || 'Something went wrong!')
  }
}

export async function sendGetDrive(drive_id) {
  try {
    const data = await api(`${API_URL}/api/admin/drives/${drive_id}`)
    return data
    
  } catch (e) {
    showToast('Admin Dashboard', e.message || 'Something went wrong!')
  }
}