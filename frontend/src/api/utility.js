export async function api(url, options = {}) {
    try {
    let access_token = getAccessToken()
    let res = await fetch(url, {
      ...options,
      headers: {
        Authorization: `Bearer ${access_token}`,
        ...(options.headers || {}),
      },
    })

    if (res.ok) {
      let data = await res.json()
      return data
    }

    throw res
  } catch (e) {
    throw await e.json()
  }
}

function getAccessToken() {
  const access_token = localStorage.getItem('access_token')
  if (!access_token) {
    throw({message: "Unauthorised user! Relogin to contine."})
  }
  return access_token
}