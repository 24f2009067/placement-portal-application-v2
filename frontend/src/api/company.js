import { showToast } from '@/toast'
import { api } from './utility'

const API_URL = import.meta.env.VITE_API_URL

export async function getCompanyProfile() {
  try {
    let access_token = getAccessToken()

    const res = await fetch(`${API_URL}/api/company`, {
      method: 'GET',
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
        name: '',
        industry: '',
        location: '',
        website: '',
      }
    }

    return data
  } catch (err) {
    showToast('Admin Dashboard', err.message || 'Something went wrong!')
    return {
      status: 'error',
      message: 'Unable to connect to server',
      error: err,
    }
  }
}

export async function setProfile(profile) {
  try {
    let access_token = getAccessToken()

    const res = await fetch(`${API_URL}/api/company`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${access_token}`,
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        name: profile.name,
        industry: profile.industry,
        location: profile.location,
        website: profile.website,
      }),
    })

    const data = await res.json()
    if (res.ok) {
      return data
    }

    console.log(data)
  } catch (err) {
    showToast('Admin Dashboard', err.message || 'Something went wrong!')
    return {
      status: 'error',
      message: 'Unable to connect to server',
      error: err,
    }
  }
}

export async function loadDashboard(s) {
  try {
    const data = await api(`${API_URL}/api/company/dashboard?search=${s}`)
    return data.data
  } catch (e) {
    showToast('Company Dashboard', e.message || 'Something went wrong!')
  }
}

export async function sendCloseDrive(drive_id) {
  try {
    const data = await api(`${API_URL}/api/company/drives/${drive_id}/close`, { method: 'PUT' })
    return data
  } catch (e) {
    showToast('Company Dashboard', e.message || 'Something went wrong!')
  }
}

export async function createDrive(drive) {
  try {
    const data = await api(`${API_URL}/api/company/drives`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify(drive),
    })
    return data
  } catch (e) {
    showToast('Company Dashboard', e.message || 'Something went wrong!')
  }
}

export async function getDrive(drive_id) {
  try {
    const data = await api(`${API_URL}/api/company/drives/${drive_id}`)
    return data
  } catch (e) {
    showToast('Company Dashboard', e.message || 'Something went wrong!')
  }
}

export async function updateDrive(drive_id, drive) {
  try {
    const data = await api(`${API_URL}/api/company/drives/${drive_id}/update`, {
      method: 'PUT',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify(drive),
    })
    return data
  } catch (e) {
    showToast('Company Dashboard', e.message || 'Something went wrong!')
  }
}

export async function modifyApplication(application_id, status, interview, placement) {
  try {
    let body = ""
    if (status === "selected"){
      body = JSON.stringify(placement)
      status = "select"
    }
    else if (status === "shortlisted"){
      body = JSON.stringify(interview)
      status = "shortlist"
    }
    else if (status === "rejected"){
      status = "reject"
    }

    const data = await api(`${API_URL}/api/company/applications/${application_id}/${status}`, {
      method: 'PUT',
      headers: {
        'content-type': 'application/json',
      },
      body: body,
    })
    return data
  } catch (e) {
    showToast('Company Dashboard', e.message || 'Something went wrong!')
  }
}

// utitities

function getAccessToken() {
  const access_token = localStorage.getItem('access_token')
  if (!access_token) {
    throw { message: 'Unauthorised user! Relogin to contine.' }
  }
  return access_token
}
