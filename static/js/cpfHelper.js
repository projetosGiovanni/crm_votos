function filtroCPF(cpf) {
  //   console.log(cpf);
  cpf = cpf.replace(/\D/g, "");
  cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
  cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
  cpf = cpf.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
  return cpf;
}

function formatCPF(event) {
  const cpfFieldElement = document.getElementById("id_cpf");
  const formattedCPF = filtroCPF(event.target.value);
  cpfFieldElement.value = formattedCPF;
}

console.log("Script carregado!");
const cpfField = document.getElementById("id_cpf");
cpfField.addEventListener("keydown", formatCPF);
