import { showToast } from "@/toast"

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
    showToast("Admin Dashboard", err.message || "Something went wrong!");
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
    showToast("Admin Dashboard", err.message || "Something went wrong!");
    return {
      status: 'error',
      message: 'Unable to connect to server',
      error: err,
    }
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