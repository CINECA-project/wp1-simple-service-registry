import React, { Component } from 'react';
import './GetServicesTable.css';

class GetServicesTable extends Component {
    constructor(props){
        super(props);
        this.state = {
            error : null,
            isLoaded : false,
            filterValue: '',
            services : []
        };
    }

    componentDidMount() {
        fetch(process.env.REACT_APP_API_SERVER)
        .then( response => response.json())
        .then(
            // handle the result
            (result) => {
                this.setState({
                    isLoaded : true,
                    services : result
                });
            },

            // Handle error 
            (error) => {
                this.setState({
                    isLoaded: true,
                    error
                })
            },
        )
    }

    cohortItems(cohort, categoryName) {
        const category = cohort.categories.filter(cat => (cat.name === categoryName));
        const valid_subcategories = category[0].subcategories.filter(subcat => ("ontologyLabel" in subcat && "value" in subcat));
        /* sex and gender are sent with ontological codes which are confusing in this UI, for now we'll skip them*/
        const valid_subcategories_nocoded = valid_subcategories.filter(subcat => !["Gender", "Sex"].includes(subcat["ontologyLabel"]));
        return valid_subcategories_nocoded.map(subcat => (<li><b>{subcat.ontologyLabel}:</b> {subcat.value}</li>));
    }

    cohortEntry(cohort) {
        const result =
            <div className="cohort">
            <b>{cohort.cohortName}:</b><br></br>
            <div className="cohortmetadata">
            <p>Basic Attributes</p>
            <ul>
            {this.cohortItems(cohort, "basic cohort attributes")}
            </ul>
            Genomic Data
            <ul>
            {this.cohortItems(cohort, "laboratory measures (Laboratory Procedure NCIT:C25294)")}
            </ul>
            </div>
            </div>;
        return result;
    }

    serviceEntry(service) {
        var servicerow = [<tr key={service.id} align="start" className="service">
                             <td className="body"><a href={service.organization.url}>{service.organization.name}</a></td>
                             <td className="user">{service.name}</td>
                             <td className="user">{service.type.group}.{service.type.artifact} {service.type.version}</td>
                             <td className="title"><a href={service.url}>service</a>, <a href={service.documentationUrl}>web</a></td>
                         </tr>];
        if ("cohorts" in service ) {
            const cohorts = [ 
                <tr className="cohorts" align="start">
                    <td colSpan="4">
                        { service.cohorts.map(cohort => this.cohortEntry(cohort)) }
                    </td>
                </tr> ];
            servicerow = servicerow.concat(cohorts);
        } else {
            const cohorts = [
                <tr className="cohorts" align="start">
                <td colSpan="4">
                <div classname="cohort">
                <p>No cohort data provided</p>
                </div>
                </td>
            </tr>];
            servicerow = servicerow.concat(cohorts);
        }
        return servicerow;
    }

    serviceCohortsMatch(service, target) {
        if (!service)
            return false;

        if (target == "")
            return true;

        if (!("cohorts" in service))
            return false;

        const cohortnames = service.cohorts.map(cohort => cohort.cohortName);
        if (cohortnames.some(name => (name.includes(target))))
            return true;

        const subcategory_values = service.cohorts.flatMap(cohort => (cohort.categories.flatMap(category => category.subcategories.flatMap(subcat => subcat.value))));
        if (subcategory_values.some(value => (value.includes(target))))
            return true;

        return false;
    }

    render() {
        const {error, isLoaded, filterValue, services } = this.state;

        if(error){
            return <div>Error in loading</div>
        }else if (!isLoaded) {
            return <div>Loading ...</div>
        }else{

            /* const filteredServices = services.filter(service => service.organization.name.includes(filterValue)); */
            const filteredServices = services.filter(service => this.serviceCohortsMatch(service, filterValue));

            return(
                <div>
                    <form onSubmit={this.handleSubmit}>
                        <label>Fiter Cohorts By
                            <input type="text" value={this.state.filterValue} onChange={e => this.setState({filterValue: e.target.value})} />
                        </label>
                    </form>

                    <table className="serviceTable">
                        <thead>
                        <tr>
                            <th>Organization</th>
                            <th>Name</th>
                            <th>Type</th>
                            <th>Url</th>
                        </tr>
                        </thead>
                        <tbody>
                        { filteredServices.map(service => this.serviceEntry(service)) }
                        </tbody>
                    </table>
                </div>
            );
        }
    }
}

export default GetServicesTable;
