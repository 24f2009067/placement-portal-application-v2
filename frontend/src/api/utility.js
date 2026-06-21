export async function api(url, options = {}) {
    try {
    let access_token = getAccessToken()
    let res = await fetch(url, {
      headers: {
        Authorization: `Bearer ${access_token}`,
        ...(options.headers || {}),
      },
      ...options,
    })

    if (res.ok) {
      let data = await res.json()
      return data
    }

    throw res
  } catch (e) {
    console.log(e)
    throw e
  }
}

function getAccessToken() {
  const access_token = localStorage.getItem('access_token')
  if (!access_token) {
    throw({message: "Unauthorised user! Relogin to contine."})
  }
  return access_token
}