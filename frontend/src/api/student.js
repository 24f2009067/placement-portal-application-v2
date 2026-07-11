import { showToast } from "@/toast"
import { api } from "./utility"

const API_URL = import.meta.env.VITE_API_URL

export async function getStudentProfile() {
  try {
    let access_token = getAccessToken()

    const res = await fetch(`${API_URL}/api/students`, {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    })
    const data = await res.json()

    if (res.ok) {
      if (data.profile_complete) {
        return data.profile
      }

      return {
        email: data.email,
        student_id: '',
        name: '',
        skills: '',
        dept: '',
        course: '',
        cgpa: '',
        graduation_year: '',
        backlog_count: '',
        resume: '',
      }
    }

    return data
  } catch (err) {
    showToast("Admin Dashboard", err.message || "Something went wrong!");
    return {
      status: 'error',
      message: 'Unable to connect to server',
      error: err,
    }
  }
}

export async function setProfile(formData) {
  try {
    let access_token = getAccessToken()

    const res = await fetch(`${API_URL}/api/students`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
      body: formData,
    })

    const data = await res.json()
    if (res.ok){
        return data
    }

    console.log(data)

  } catch (err) {
    showToast("Admin Dashboard", err.message || "Something went wrong!");
    return {
      status: 'error',
      message: 'Unable to connect to server',
      error: err,
    }
  }
}

// dashboard

export async function loadDashboard(s) {
  try {
    const data = await api(`${API_URL}/api/students/dashboard?search=${s}`)
    return data.data
  } catch (e) {
    showToast('Student Dashboard', e.message || 'Something went wrong!')
  }
}

export async function getCompany(user_id) {
  try {
    const data = await api(`${API_URL}/api/students/company/${user_id}`)
    return data
  } catch (e) {
    showToast('Student Dashboard', e.message || 'Something went wrong!')
  }
}

export async function getDrive(drive_id) {
  try {
    const data = await api(`${API_URL}/api/students/drives/${drive_id}`)
    return data
  } catch (e) {
    showToast('Student Dashboard', e.message || 'Something went wrong!')
  }
}

export async function applyDrive(drive_id) {
  try {
    const data = await api(`${API_URL}/api/students/drives/${drive_id}/applications`, {method: "POST"})
    return data
  } catch (e) {
    showToast('Student Dashboard', e.message || 'Something went wrong!')
  }
}

export async function getNotifications() {
  try {
    const data = await api(`${API_URL}/api/students/notifications`)
    return data
  } catch (e) {
    showToast('Student Dashboard', e.message || 'Something went wrong!')
  }
}

export async function markRead(notification_id) {
  try {
    const data = await api(`${API_URL}/api/students/notifications/${notification_id}/seen`, {method: "PUT"})
    return data
  } catch (e) {
    showToast('Student Dashboard', e.message || 'Something went wrong!')
  }
}

export async function getHistory() {
  try {
    const data = await api(`${API_URL}/api/students/history`)
    return data
  } catch (e) {
    showToast('Student Dashboard', e.message || 'Something went wrong!')
  }
}

// backend jobs

export async function generateReport() {
  try {
    const data = await api(`${API_URL}/api/students/report`, {method: "POST"})
    return data
  } catch (e) {
    showToast('Student Dashboard', e.message || 'Something went wrong!')
  }
}

// utitities

function getAccessToken() {
  const access_token = localStorage.getItem('access_token')
  if (!access_token) {
    throw({message: "Unauthorised user! Relogin to contine."})
  }
  return access_token
}