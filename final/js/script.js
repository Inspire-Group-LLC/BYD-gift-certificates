const apiUrl = 'https://c5bc-195-158-20-242.ngrok-free.app';

const state = {
  users_url: `${apiUrl}/api/users/`,
  certificates_url: `${apiUrl}/api/certificates`,
  create_url: `${apiUrl}/api/certificates/create/`,
  login_url: `${apiUrl}/login/`,
  registrate_url: `${apiUrl}/signup/`,
  transfer_url: `${apiUrl}/api/certificates/transfer/`,
};

const cacheState = () => {
  state.elements = {
    certificates_table: document.getElementById("certificates-table"),
    sort_by_name: document.getElementById("sort-by-name"),
    table_th: document.getElementById("table-th"),
    sort_by_price: document.getElementById("sort-by-price"),
    submit_new_sertificate: document.getElementById("submit_new_sertificate"),
    new_sertificate: document.getElementById("new-sertificate"),
    newSertificateBtn: document.querySelector(".newSertificate"),
    login_form: document.getElementById("login_form"),
    registration_form: document.getElementById("registration_form"),
    registration_page: document.querySelector(".registration_page"),
    login_page: document.querySelector(".login_page"),
    logout_btn: document.getElementById("logout"),
    table_page: document.getElementById("table_page"),
    page_heading: document.getElementById("page_heading"),
    registration_page_link: document.getElementById("registration_page_link"),
    login_page_link: document.getElementById("login_page_link"),
    transfer: document.getElementById("transfer"),
    open_transfer_btn: document.getElementById("open_transfer_btn"),
    transfer_form: document.getElementById("transfer_form"),
    close_create: document.getElementById("close_create"),
    close_transfer: document.getElementById("close_transfer"),
    search_filter: document.getElementById("search_filter"),
  };
};


const renderCertificates = (certificates) => {
  const certificates_table = state.elements.certificates_table;
  const first_row = certificates_table.querySelector('#table_th');
  certificates_table.innerHTML = "";
  certificates_table.appendChild(first_row);

  certificates.forEach((certificate) => {
    certificates_table.insertAdjacentHTML("beforeend", `
      <tr>
        <td><div><input type="checkbox"></div></td>
        <td class="tdtable"><div>${certificate?.user?.full_name}</div></td>
        <td class="tdtable"><div>${certificate.unique_string}</div></td>
        <td class="tdtable"><div>${certificate.price}$</div></td>
        <td><div><img src="img/dots-horizontal.svg" alt=""></div></td>
      </tr>
    `);
  });
};

const fetchData = async (url, options) => {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

const showAlert = (message) => {
  alert(message);
};

const clearInputValues = (inputs) => {
  inputs.forEach((input) => {
    input.value = "";
  });
};

const toggleElementVisibility = (element) => {
  element.classList.toggle("hidden");
};

const loginFromSubmit = async (e) => {
  e.preventDefault();
  const usernameInput = state.elements.login_form.querySelector("[name='username']");
  const passwordInput = state.elements.login_form.querySelector("[name='password']");
  const username = usernameInput.value;
  const password = passwordInput.value;

  const options = {
    method: "POST",
    body: JSON.stringify({ username, password }),
    headers: {
      "Content-Type": "application/json",
    },
  };

  try {
    const data = await fetchData(state.login_url, options);
    const random = Math.random().toString(36).substring(7);
    sessionStorage.setItem("username", username + "&&" + random);
    state.elements.login_page.classList.add("hidden");
    localStorage.setItem("user_id", data.user_id);
    localStorage.setItem("is_superuser", data.is_superuser);
    hideAdminFunctions();
    await renderUserCertificates();
  } catch (error) {
    console.error("Login failed:", error.message);
    showAlert("Wrong username or password");
    clearInputValues([usernameInput, passwordInput]);
  }
};

const getCertificates = async (search) => {
  const url = state.certificates_url + `/?userid=${localStorage.getItem("user_id")}&search=${search ? search : ""}`;
  return await fetchData(url);
};


// const sortByName = () => {
//   const certificates_table = state.elements.certificates_table;
//   if(certificates_table.classList.contains("sort_created")) {
//     renderCertificates();
//   } else {
//     renderCertificates("?order=asc");
//   }
//   certificates_table.classList.toggle("sort_created");
// };

// const sortByPrice = () => {
//   const certificates_table = state.elements.certificates_table;
//   const first_row = certificates_table.firstElementChild;
//   certificates_table.innerHTML = "";
//   certificates_table.appendChild(first_row);
//   if(certificates_table.classList.contains("sort_price")) {
//     renderCertificates("?price=asc");
//   } else {
//     renderCertificates("?price=desc");
//   }
//   certificates_table.classList.toggle("sort_price");
// }

const createCertificate = async () => {
  toggleElementVisibility(state.elements.new_sertificate);
  const unique_string = state.elements.new_sertificate.querySelector("#unique_string").value;
  let price = state.elements.new_sertificate.querySelector("#price").value;
  let phone = state.elements.new_sertificate.querySelector("#phone").value;
  price = parseFloat(price);

  if (!unique_string || !price || !phone) {
    showAlert("Please fill all fields");
    return;
  }

  const options = {
    method: "POST",
    body: JSON.stringify({ unique_string, price, "phone_number": phone }),
    headers: {
      "Content-Type": "application/json",
    },
  };

  try {
    await fetchData(state.create_url, options);
    showAlert("Certificate is created");
    renderUserCertificates();
  } catch (error) {
    console.error("Certificate creation failed:", error.message);
    showAlert("This certificate is already exist");
    clearInputValues(state.elements.new_sertificate.querySelectorAll("input"));
  }
};

const transferCertificate = async (e) => {
  e.preventDefault();
  const unique_string = state.elements.transfer_form.querySelector("[name='unique_string']").value;
  const phone_number = state.elements.transfer_form.querySelector("[name='phone_number']").value;
  const user_id = Number(localStorage.getItem("user_id"));

  if (!unique_string || !phone_number) {
    showAlert("Please fill all fields");
    return;
  }

  const options = {
    method: "POST",
    body: JSON.stringify({ "user_id": user_id, phone_number, unique_string }),
    headers: {
      "Content-Type": "application/json",
    },
  };

  try {
    await fetchData(state.transfer_url, options);
    showAlert("Certificate is transferred");
    toggleElementVisibility(state.elements.transfer);
    renderUserCertificates();
  } catch (error) {
    console.error("Certificate transfer failed:", error.message);
    showAlert("Something went wrong");
    clearInputValues(state.elements.transfer_form.querySelectorAll("input"));
  }
};

const renderUserCertificates = async () => {
  state.elements.table_page.classList.remove("hidden");
  const certificates = await getCertificates();
  renderCertificates(certificates);
};

const searchResults = async (e) => {
  const search = state.elements.search_filter.value;
  if (search.length < 3) {
    renderUserCertificates();
    return;
  }
  const certificates = await getCertificates(search);
  renderCertificates(certificates);
};

const registerUser = async (e) => {
  e.preventDefault();
  const full_name = state.elements.registration_form.querySelector("[name='full_name']").value;
  const phone_number = state.elements.registration_form.querySelector("[name='phone_number']").value;
  const username = state.elements.registration_form.querySelector("[name='username']").value;
  const password = state.elements.registration_form.querySelector("[name='password']").value;

  await fetch(state.registrate_url, {
    method: "POST",
    body: JSON.stringify({
      full_name,
      phone_number,
      username,
      password
    }),
    headers: {
      "Content-Type": "application/json"
    }
  }).then(async (response) => {
    if(!response.ok) {
      alert("This username is already exist");
      state.elements.registration_form.querySelectorAll("input").forEach((input) => {
        input.value = "";
      });
    } else {
      const data = await response.json();
      const random = Math.random().toString(36).substring(7);
      sessionStorage.setItem("username", username + "&&" + random);
      state.elements.registration_page.classList.add("hidden");
      localStorage.setItem("user_id", data.user_id);
      localStorage.setItem("is_superuser", data.is_superuser);
      hideAdminFunctions();
      await renderUserCertificates();
    }
  }).catch((error) => {
    console.log(error);
  });
};

const debounce = (func, wait, immediate) => {
  var timeout;
  return function() {
   var context = this, args = arguments;
   clearTimeout(timeout);
   if (immediate && !timeout) func.apply(context, args);
   timeout = setTimeout(function() {
    timeout = null;
    if (!immediate) func.apply(context, args);
   }, wait);
  };
}

const hideAdminFunctions = () => {
  if(localStorage.getItem("is_superuser") == "false") {
    state.elements.page_heading.innerHTML = "My certificates - " + sessionStorage?.getItem("username")?.split("&&")[0];
    state.elements.newSertificateBtn.classList.add("hidden");  
  } else {
    state.elements.page_heading.innerHTML = "Certificates - Admin";
    state.elements.newSertificateBtn.classList.remove("hidden");   
  }
}

const logout = () => {
  sessionStorage.removeItem("username");
  localStorage.removeItem("user_id");
  state.elements.table_page.classList.add("hidden");
  state.elements.login_page.classList.remove("hidden");
  checkUserLoggedIn();
}

const openPage = (page) => {
  state.elements.registration_page.classList.add("hidden");
  state.elements.login_page.classList.add("hidden");
  state.elements.table_page.classList.add("hidden");
  state.elements[page].classList.remove("hidden");
}

const addEventListeners = () => {
  // state.elements.sort_by_name.addEventListener("click", sortByName);
  // state.elements.sort_by_price.addEventListener("click", sortByPrice);
  state.elements.submit_new_sertificate.addEventListener("click", createCertificate);
  state.elements.newSertificateBtn.addEventListener("click", () => {
    state.elements.new_sertificate.classList.toggle("hidden");
  });
  state.elements.login_form.addEventListener("submit", loginFromSubmit);
  state.elements.logout_btn.addEventListener("click", logout);
  state.elements.registration_page_link.addEventListener("click", () => {
    openPage("registration_page");
  });
  state.elements.login_page_link.addEventListener("click", () => {
    openPage("login_page");
  });
  state.elements.registration_form.addEventListener("submit", registerUser);
  state.elements.open_transfer_btn.addEventListener("click", () => {
    state.elements.transfer.classList.toggle("hidden");
  });
  state.elements.transfer_form.addEventListener("submit", transferCertificate);
  state.elements.close_create.addEventListener("click", () => {
    state.elements.new_sertificate.classList.toggle("hidden");
  });
  state.elements.close_transfer.addEventListener("click", () => {
    state.elements.transfer.classList.toggle("hidden");
  });
  state.elements.search_filter.addEventListener("input", debounce(searchResults, 500));
}

const checkUserLoggedIn = async () => {
  const username = sessionStorage.getItem("username");
  hideAdminFunctions();
  if(!username) {
    state.elements.login_page.classList.remove("hidden");
    return;
  } else {
    state.elements.login_page.classList.add("hidden");
    await renderUserCertificates();
  }
}

const init = () => {
  cacheState();
  addEventListeners();
  checkUserLoggedIn();
};

document.addEventListener("DOMContentLoaded", init);
