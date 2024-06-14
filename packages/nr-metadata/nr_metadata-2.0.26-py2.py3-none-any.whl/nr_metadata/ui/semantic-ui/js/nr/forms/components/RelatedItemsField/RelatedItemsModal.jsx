// This file is part of Invenio-RDM-Records
// Copyright (C) 2020-2023 CERN.
// Copyright (C) 2020-2022 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
// Copyright (C) 2022 data-futures.org.
//
// Invenio-RDM-Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import { Button, Form, Grid, Header, Modal } from "semantic-ui-react";
import { Formik } from "formik";
import * as Yup from "yup";
import { i18next } from "@translations/nr/i18next";
import { TextField, FieldLabel, GroupField } from "react-invenio-forms";
import { CreatibutorsField } from "../CreatibutorsField";
import {
  IdentifiersField,
  objectIdentifiersSchema,
  IdentifiersValidationSchema,
} from "../IdentifiersField";
import { LocalVocabularySelectField } from "@js/oarepo_vocabularies";
import PropTypes from "prop-types";
import {
  requiredMessage,
  handleValidateAndBlur,
  sanitizeInput,
} from "@js/oarepo_ui";
import { getIn } from "formik";

const RelatedItemsSchema = Yup.object({
  itemTitle: Yup.string().required(requiredMessage).label(i18next.t("Title")),
  itemURL: Yup.string().url(i18next.t("Please provide an URL in valid format")),
  itemYear: Yup.number()
    .typeError(i18next.t("Year must be a number."))
    .test("len", i18next.t("Year must be in format YYYY."), (val) => {
      if (val) {
        return val.toString().length === 4;
      }
      return true;
    }),
  itemPIDs: IdentifiersValidationSchema,
  itemVolume: Yup.string(),
  itemIssue: Yup.string(),
  itemStartPage: Yup.string(),
  itemEndPage: Yup.string(),
  itemPublisher: Yup.string(),
  itemRelationType: Yup.object(),
  itemResourceType: Yup.object(),
});

const modalActions = {
  ADD: "add",
  EDIT: "edit",
};
export const RelatedItemsModal = ({
  initialRelatedItem,
  initialAction,
  addLabel,
  editLabel,
  onRelatedItemChange,
  trigger,
  validTags,
}) => {
  const [open, setOpen] = React.useState(false);
  const [action, setAction] = React.useState(initialAction);
  const [saveAndContinueLabel, setSaveAndContinueLabel] = React.useState(
    i18next.t("Save and add another")
  );

  const openModal = () => {
    setOpen(true);
  };
  const closeModal = () => {
    setOpen(false);
  };

  const changeContent = () => {
    setSaveAndContinueLabel(i18next.t("Added"));
    setTimeout(() => {
      setSaveAndContinueLabel(i18next.t("Save and add another"));
    }, 1000);
  };

  const onSubmit = (values, formikBag) => {
    const fieldValue = getIn(values, "itemTitle");
    const cleanedContent = sanitizeInput(fieldValue, validTags);
    const updatedValues = { ...values, itemTitle: cleanedContent };
    onRelatedItemChange(updatedValues);
    formikBag.setSubmitting(false);
    formikBag.resetForm();
    switch (action) {
      case "saveAndContinue":
        closeModal();
        setAction(initialAction);
        openModal();
        changeContent();
        break;
      case "saveAndClose":
        closeModal();
        setAction(initialAction);
        break;
      default:
        break;
    }
  };

  return (
    <Formik
      initialValues={initialRelatedItem || {}}
      onSubmit={onSubmit}
      enableReinitialize
      validationSchema={RelatedItemsSchema}
      validateOnChange={false}
      validateOnBlur={false}
    >
      {({
        values,
        resetForm,
        handleSubmit,
        validateField,
        setFieldTouched,
      }) => {
        const handleBlur = handleValidateAndBlur(
          validateField,
          setFieldTouched
        );
        return (
          <Modal
            className="form-modal"
            size="large"
            centered={false}
            onOpen={() => openModal()}
            open={open}
            trigger={trigger}
            onClose={() => {
              closeModal();
              resetForm();
            }}
            closeIcon
            closeOnDimmerClick={false}
          >
            <Modal.Header as="h6">
              <Grid>
                <Grid.Column floated="left" width={8}>
                  <Header as="h2">
                    {action === modalActions.ADD ? addLabel : editLabel}
                  </Header>
                </Grid.Column>
              </Grid>
            </Modal.Header>
            <Modal.Content>
              <Form>
                <TextField
                  autoComplete="off"
                  fieldPath="itemTitle"
                  required
                  label={
                    <FieldLabel
                      htmlFor={"itemTitle"}
                      icon="pencil"
                      label={i18next.t("Title")}
                    />
                  }
                  onBlur={() => handleBlur("itemTitle")}
                />
                <CreatibutorsField
                  label={i18next.t("Creators")}
                  labelIcon="user"
                  fieldPath="itemCreators"
                  schema="creators"
                  autocompleteNames="off"
                  required={false}
                />

                <CreatibutorsField
                  label={i18next.t("Contributors")}
                  addButtonLabel={i18next.t("Add contributor")}
                  modal={{
                    addLabel: i18next.t("Add contributor"),
                    editLabel: i18next.t("Edit contributor"),
                  }}
                  labelIcon="user"
                  fieldPath="itemContributors"
                  schema="contributors"
                  autocompleteNames="off"
                />

                <IdentifiersField
                  className="related-items-identifiers"
                  options={objectIdentifiersSchema}
                  fieldPath="itemPIDs"
                  identifierLabel={i18next.t("Object identifier")}
                  label={i18next.t("Identifier")}
                  helpText={i18next.t(
                    "Persistent identifier/s of object as ISBN, DOI, etc."
                  )}
                  validateOnBlur
                />
                <TextField
                  autoComplete="off"
                  fieldPath="itemURL"
                  label={
                    <FieldLabel
                      htmlFor={"itemURL"}
                      icon="pencil"
                      label={i18next.t("URL")}
                    />
                  }
                  onBlur={() => handleBlur("itemURL")}
                />
                <GroupField widths="equal">
                  <TextField
                    fieldPath="itemYear"
                    label={
                      <FieldLabel
                        htmlFor={"itemYear"}
                        icon="pencil"
                        label={i18next.t("Year")}
                      />
                    }
                    onBlur={() => handleBlur("itemYear")}
                  />
                  <TextField
                    fieldPath="itemVolume"
                    label={
                      <FieldLabel
                        htmlFor={"itemVolume"}
                        icon="pencil"
                        label={i18next.t("Volume")}
                      />
                    }
                    onBlur={() => handleBlur("itemVolume")}
                  />
                  <TextField
                    fieldPath="itemIssue"
                    label={
                      <FieldLabel
                        htmlFor={"itemIssue"}
                        icon="pencil"
                        label={i18next.t("Issue")}
                      />
                    }
                    onBlur={() => handleBlur("itemIssue")}
                  />
                  <TextField
                    fieldPath="itemStartPage"
                    label={
                      <FieldLabel
                        htmlFor={"itemStartPage"}
                        icon="pencil"
                        label={i18next.t("Start page")}
                      />
                    }
                    onBlur={() => handleBlur("itemStartPage")}
                  />
                  <TextField
                    fieldPath="itemEndPage"
                    label={
                      <FieldLabel
                        htmlFor={"itemEndPage"}
                        icon="pencil"
                        label={i18next.t("End page")}
                      />
                    }
                    onBlur={() => handleBlur("itemEndPage")}
                  />
                </GroupField>
                <TextField
                  width={16}
                  fieldPath="itemPublisher"
                  label={
                    <FieldLabel
                      htmlFor={"itemPublisher"}
                      icon="pencil"
                      label={i18next.t("Publisher")}
                    />
                  }
                  onBlur={() => handleBlur("itemPublisher")}
                />
                <GroupField>
                  <LocalVocabularySelectField
                    width={16}
                    fieldPath="itemRelationType"
                    label={
                      <FieldLabel
                        htmlFor={"itemRelationType"}
                        icon="pencil"
                        label={i18next.t("Relation type")}
                      />
                    }
                    placeholder={i18next.t("Choose relation type")}
                    clearable
                    optionsListName="item-relation-types"
                  />
                  <LocalVocabularySelectField
                    width={16}
                    fieldPath="itemResourceType"
                    clearable
                    label={
                      <FieldLabel
                        htmlFor={"itemResourceType"}
                        icon="tag"
                        label={i18next.t("Resource type")}
                      />
                    }
                    placeholder={i18next.t("Select resource type")}
                    optionsListName="resource-types"
                  />
                </GroupField>
              </Form>
            </Modal.Content>
            <Modal.Actions>
              <Button
                name="cancel"
                onClick={() => {
                  resetForm();
                  closeModal();
                }}
                icon="remove"
                content={i18next.t("Cancel")}
                floated="left"
              />

              {action === modalActions.ADD && (
                <Button
                  name="submit"
                  type="submit"
                  onClick={() => {
                    setAction("saveAndContinue");
                    handleSubmit();
                  }}
                  primary
                  icon="checkmark"
                  content={saveAndContinueLabel}
                />
              )}
              <Button
                name="submit"
                type="submit"
                onClick={() => {
                  setAction("saveAndClose");
                  handleSubmit();
                }}
                primary
                icon="checkmark"
                content={i18next.t("Save")}
              />
            </Modal.Actions>
          </Modal>
        );
      }}
    </Formik>
  );
};

RelatedItemsModal.propTypes = {
  initialRelatedItem: PropTypes.object,
  initialAction: PropTypes.string.isRequired,
  addLabel: PropTypes.string,
  editLabel: PropTypes.string,
  onRelatedItemChange: PropTypes.func,
  trigger: PropTypes.node,
  validTags: PropTypes.array,
};

RelatedItemsModal.defaultProps = {
  initialRelatedItem: {},
};
