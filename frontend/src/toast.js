import { reactive } from "vue"

export const toasts = reactive([])

export function showToast(title, message, type = "success") {
  const id = Date.now()

  toasts.push({
    id,
    title,
    message,
    type
  })

  setTimeout(() => {
    const index = toasts.findIndex(t => t.id === id)

    if (index !== -1) {
      toasts.splice(index, 1)
    }
  }, 4000)
}