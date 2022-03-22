// https = require('https')

const defaults = {
  hostname: 'todo.local.noop.app',
  port: 443,
  path: '/api/item',
  method: 'GET'
}

function deleteItem(id) {
  console.log(`deleting ${id}`)
  $.ajax({
    url: `https://todo.local.noop.app/api/item/${id}`,
    type: 'DELETE',
    success: function (result) {
      console.log(result)
    }
  })
  window.location.reload(true)

}

function updateItem(id) {
  console.log(`updating ${id}`)
}
