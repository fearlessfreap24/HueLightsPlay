async function get_diamond_number(){
    let resp = await fetch('/api/v1/get_diamond_numbers');
    let data = await resp.json();
    return data;
};

async function get_bush_count(){
    let resp = await fetch('/api/v1/get_bush_count');
    let data = await resp.json();
    return data;
};

async function get_bush_diamonds(){
    let resp = await fetch('/api/v1/get_bush_diamonds');
    let data = await resp.json();
    return data;
};

async function main(){
    let diamonds = await get_diamond_number();
    let bushes = await get_bush_count();
    let bush_diamonds = await get_bush_diamonds();
    let bar_diamonds_labels = Object.keys(diamonds)
    let bar_diamonds_values = Object.values(diamonds)
    let bush_count_labels = Object.keys(bushes)
    let bush_count_values = Object.values(bushes)
    let bush_diamonds_labels = Object.keys(bush_diamonds)
    let bush_diamonds_values = Object.values(bush_diamonds)

    let bar_data = {
        labels: bar_diamonds_labels,
        datasets: [{
            label: "Diamonds Received By Bush Type",
            backgroundColor: [
                'rgb(245,117,240)',
                'rgb(247,211,63)',
                'rgb(250,123,39)',
                'rgb(76,0,153)',
                'rgb(204,204,0)'
            ],
            borderColor: 'rgb(77, 25, 121)',
            data: bar_diamonds_values
        }]
    }

    let bar_config = {
        type: bar,
        data: bar_data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    }
};

main();


// stuff from html
// fetch('/api/v1/get_diamond_numbers')
//         .then(resp => resp.json())
//         .then(ddata => {
//             // console.log(ddata)
//             const labels = Object.keys(ddata);
//             const data = {
//               labels: labels,
//               datasets: [{
//                 label: 'Diamonds Received by Bush Type',
//                 backgroundColor: [
//                 'rgb(245,117,240)',
//                 'rgb(247,211,63)',
//                 'rgb(250,123,39)',
//                 'rgb(76,0,153)',
//                 'rgb(204,204,0)'
//               ],
//                 borderColor: 'rgb(77, 25, 121)',
//                 data: Object.values(ddata),
//               }]
//             };
//             const config = {
//                 type: 'bar',
//                 data: data,
//                 options: {
//                   scales: {
//                     y: {
//                       beginAtZero: true
//                     }
//                   }
//                 },
//               };
    
//             const myChart = new Chart(
//             document.getElementById('diamonds'),
//             config
//             );
//         })

      
        // fetch('/api/v1/get_bush_count')
        // .then(resp => resp.json())
        // .then(bdata => {
        //     // console.log(bdata)
        //     const labels = Object.keys(bdata)
        //     const data = {
        //         labels: labels,
        //         datasets: [{
        //           label: 'Bush Counts',
        //           data: Object.values(bdata),
        //           backgroundColor: [
        //             'rgb(245,117,240)',
        //             'rgb(247,211,63)',
        //             'rgb(250,123,39)',
        //             'rgb(76,0,153)',
        //             'rgb(204,204,0)'
        //           ],
        //           hoverOffset: 4
        //         }]
        //       };
        //     const config = {
        //         type: 'pie',
        //         data: data
        //     }
        //     const myChart = new Chart(
        //     document.getElementById('bushes'),
        //     config
        //     );
        // })
      