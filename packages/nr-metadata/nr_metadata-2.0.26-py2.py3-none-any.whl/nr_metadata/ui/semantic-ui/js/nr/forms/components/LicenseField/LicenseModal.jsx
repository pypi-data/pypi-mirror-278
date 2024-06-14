// This file is part of React-Invenio-Deposit
// Copyright (C) 2020 CERN.
// Copyright (C) 2020-2022 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
//
// React-Invenio-Deposit is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/nr/i18next";
import { Formik, getIn } from "formik";
import PropTypes from "prop-types";
import React, { Component } from "react";
import { OverridableContext } from "react-overridable";
import {
  EmptyResults,
  Error,
  InvenioSearchApi,
  ReactSearchKit,
  ResultsLoader,
  SearchBar,
  Toggle,
  Pagination,
  withState,
} from "react-searchkit";
import {
  Button,
  Grid,
  Header,
  Menu,
  Modal,
  Message,
  Icon,
} from "semantic-ui-react";
import * as Yup from "yup";
import { LicenseFilter } from "./LicenseFilter";
import { LicenseResults } from "./LicenseResults";
import { EmptyResultsElement } from "@js/oarepo_ui";

const overriddenComponents = {
  "SearchFilters.Toggle": LicenseFilter,
  "EmptyResults.element": EmptyResultsElement,
};

const PaginationWrapper = withState(
  ({
    currentResultsState: {
      data: { total },
    },
  }) =>
    total > 25 && (
      <div className="text-align-center">
        <Pagination options={{ size: "mini" }} />
      </div>
    )
);
const LicenseSchema = Yup.object().shape({
  selectedLicense: Yup.object().shape({
    id: Yup.string().required(i18next.t("You must choose one license.")),
  }),
});

export class LicenseModal extends Component {
  state = {
    open: false,
  };

  openModal = () => {
    this.setState({ open: true });
  };

  closeModal = () => {
    this.setState({ open: false });
  };

  onSubmit = (values) => {
    const { handleLicenseChange } = this.props;
    this.closeModal();
    handleLicenseChange(values.selectedLicense);
  };

  render() {
    const {
      trigger,
      searchConfig,
      serializeLicense,
      initialLicense: initialLicenseProp,
    } = this.props;
    const { open } = this.state;

    const initialLicense = initialLicenseProp || {};

    const searchApi = new InvenioSearchApi(searchConfig.searchApi);
    return (
      <Formik
        initialValues={{
          selectedLicense: initialLicense,
        }}
        onSubmit={this.onSubmit}
        enableReinitialize={true}
        validationSchema={LicenseSchema}
        validateOnChange={false}
        validateOnBlur={false}
      >
        {({ handleSubmit, resetForm, errors }) => (
          <Modal
            onOpen={() => this.openModal()}
            open={open}
            trigger={trigger}
            onClose={this.closeModal}
            closeIcon
            closeOnDimmerClick={false}
          >
            <Modal.Header as="h6" className="pt-10 pb-10">
              <Grid>
                <Grid.Column width={8} floated="left">
                  <Header as="h2">{i18next.t("Choose license")}</Header>
                </Grid.Column>
              </Grid>
            </Modal.Header>
            <Modal.Content scrolling>
              <OverridableContext.Provider value={overriddenComponents}>
                <ReactSearchKit
                  searchApi={searchApi}
                  urlHandlerApi={{ enabled: false }}
                  initialQueryState={searchConfig.initialQueryState}
                >
                  <Grid>
                    <Grid.Row>
                      <Grid.Column
                        width={8}
                        floated="left"
                        verticalAlign="middle"
                      >
                        <SearchBar
                          placeholder={i18next.t("Search")}
                          autofocus
                          actionProps={{
                            icon: "search",
                            content: null,
                            className: "search",
                          }}
                        />
                      </Grid.Column>
                      <Grid.Column width={8} textAlign="right" floated="right">
                        <Menu compact size="tiny" className="license-toggler">
                          <Toggle
                            title={i18next.t("Featured")}
                            label="featured"
                            filterValue={["tags", "featured"]}
                          />
                          <Toggle
                            title={i18next.t("All")}
                            label="all"
                            // TODO: we don't have tags=all, so this is a hack to display all licenses
                            filterValue={["tags", ""]}
                          />
                        </Menu>
                      </Grid.Column>
                    </Grid.Row>
                    {getIn(errors, "selectedLicense", {}).id && (
                      <Grid.Row>
                        <Grid.Column width={8}>
                          <Message compact warning>
                            <Icon name="warning sign" />
                            {getIn(errors, "selectedLicense", {}).id}
                          </Message>
                        </Grid.Column>
                      </Grid.Row>
                    )}
                    <Grid.Row verticalAlign="middle">
                      <Grid.Column>
                        <ResultsLoader>
                          <EmptyResults />
                          <Error />
                          <LicenseResults serializeLicense={serializeLicense} />
                          <PaginationWrapper />
                        </ResultsLoader>
                      </Grid.Column>
                    </Grid.Row>
                  </Grid>
                </ReactSearchKit>
              </OverridableContext.Provider>
            </Modal.Content>
            <Modal.Actions>
              <Button
                name="cancel"
                onClick={() => {
                  resetForm();
                  this.closeModal();
                }}
                icon="remove"
                labelPosition="left"
                content={i18next.t("Cancel")}
                floated="left"
              />
              <Button
                name="submit"
                onClick={(event) => handleSubmit(event)}
                primary
                icon="checkmark"
                labelPosition="left"
                content={i18next.t("Choose license")}
              />
            </Modal.Actions>
          </Modal>
        )}
      </Formik>
    );
  }
}

LicenseModal.propTypes = {
  initialLicense: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
  trigger: PropTypes.object.isRequired,
  handleLicenseChange: PropTypes.func.isRequired,
  searchConfig: PropTypes.shape({
    searchApi: PropTypes.shape({
      axios: PropTypes.shape({
        headers: PropTypes.object,
      }),
    }).isRequired,
    initialQueryState: PropTypes.shape({
      filters: PropTypes.arrayOf(PropTypes.array),
    }).isRequired,
  }).isRequired,
  serializeLicense: PropTypes.func,
};

LicenseModal.defaultProps = {
  initialLicense: undefined,
  serializeLicense: undefined,
};
