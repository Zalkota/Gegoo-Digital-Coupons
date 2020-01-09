$(document).ready(function() {

    var UserRewardData = parseInt("{{ data }}")
    console.log(UserRewardData)

    new Chart(document.getElementById("doughnut-chart"), {
        type: 'doughnut',
        data: {

          datasets: [
            {
              label: "Population (millions)",
              backgroundColor: ["#7505AB"],
              data: [UserRewardData, 100],
              weight: 0.5,
            }
          ]
        },
        options: {

          title: {
            display: false,
          }
        }
    });


});
