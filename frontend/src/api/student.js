const API_URL = import.meta.env.VITE_API_URL

export async function getStudentProfile() {
  try {
    const access_token = localStorage.getItem('access_token')
    if (!access_token) {
      return {
        status: 'error',
        message: 'access_token not found',
      }
    }

    const res = await fetch(`${API_URL}/api/students/`, {
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
    return {
      status: 'error',
      message: 'Unable to connect to server',
      error: err,
    }
  }
}

export async function setProfile(formData) {
  try {
    const access_token = localStorage.getItem('access_token')
    if (!access_token) {
      return {
        status: 'error',
        message: 'access_token not found',
      }
    }

    const res = await fetch(`${API_URL}/api/students/`, {
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
    return {
      status: 'error',
      message: 'Unable to connect to server',
      error: err,
    }
  }
}
