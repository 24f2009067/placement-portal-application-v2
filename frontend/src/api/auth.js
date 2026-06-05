const API_URL = import.meta.env.VITE_API_URL

// registration

export async function register(email, password, role) {
  try {
    const res = await fetch(`${API_URL}/api/auth/users`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        role,
      }),
    })

    const data = await res.json()

    if (res.ok) {
      return {
        status: 'success',
        message: data.message,
      }
    }

    if (res.status === 400 || res.status === 409) {
      return {
        status: 'error',
        message: Object.values(data.message)[0],
      }
    }

    return {
      status: 'error',
      message: 'Unexpected server error',
    }
  } catch (err) {
    return {
      status: 'error',
      message: 'Unable to connect to server',
      error: err,
    }
  }
}

// login

export async function login(email, password) {
  try {
    let res = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    })

    let data = await res.json()
    if (res.status == 400) {
      return {
        status: 'error',
        message: Object.values(data.message)[0],
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

// about

// export async function isProfileComplete() {

//   let access_token = localStorage.getItem("access_token")
//   if (!access_token){
//     return {
//       status: "error",
//       message: "No accesstoken in local storage"
//     }
//   }

//   try {
//     let res = fetch(`${API_URL}/auth/users`, {
//       method: 'get',
//       headers: {
//         Authorization: `Bearer ${access_token}`
//       }
//     })

//     data = res.

//   } catch (err) {
//     return {
//       status: 'error',
//       message: 'Unable to connect to server',
//       error: err,
//     }
//   }
// }
