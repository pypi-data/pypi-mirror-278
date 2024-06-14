import React from "react";
import PropTypes from "prop-types";
import { ArrayField, SelectField, TextField } from "react-invenio-forms";
import { i18next } from "@translations/nr/i18next";
import { ArrayFieldItem, useValidateOnBlur } from "@js/oarepo_ui";
import { useFormikContext, getIn } from "formik";
import * as Yup from "yup";

export const objectIdentifiersSchema = [
  { value: "DOI", text: i18next.t("DOI"), key: "DOI" },
  { value: "Handle", text: i18next.t("Handle"), key: "Handle" },
  { value: "ISBN", text: i18next.t("ISBN"), key: "ISBN" },
  { value: "ISSN", text: i18next.t("ISSN"), key: "ISSN" },
  { value: "RIV", text: i18next.t("RIV"), key: "RIV" },
];

export const personIdentifiersSchema = [
  { value: "orcid", text: i18next.t("ORCID"), key: "orcid" },
  { value: "scopusID", text: i18next.t("ScopusID"), key: "scopusID" },
  {
    value: "researcherID",
    text: i18next.t("ResearcherID"),
    key: "researcherID",
  },
  { value: "czenasAutID", text: i18next.t("CzenasAutID"), key: "czenasAutID" },
  { value: "vedidk", text: i18next.t("vedIDK"), key: "vedidk" },
  {
    value: "institutionalID",
    text: i18next.t("InstitutionalID"),
    key: "institutionalID",
  },
  { value: "ISNI", text: i18next.t("ISNI"), key: "ISNI" },
];

export const organizationIdentifiersSchema = [
  { value: "ISNI", text: i18next.t("ISNI"), key: "ISNI" },
  { value: "ROR", text: i18next.t("ROR"), key: "ROR" },
  { value: "ICO", text: i18next.t("ICO"), key: "ICO" },
  { value: "DOI", text: i18next.t("DOI"), key: "DOI" },
];

export const IdentifiersValidationSchema = Yup.array().of(
  Yup.object().shape({
    identifier: Yup.string().test(
      "Test if both identifier and identifier type are provided",
      i18next.t("Both identifier and identifier type must be filled."),
      (value, context) => {
        if (!value && !context.parent.scheme) return true;
        return !(!value && context.parent.scheme);
      }
    ),
    scheme: Yup.string().test(
      "Test if both identifier and identifier type are provided",
      i18next.t("Both identifier and identifier type must be filled."),
      (value, context) => {
        if (!value && !context.parent.identifier) return true;
        return !(!value && context.parent.identifier);
      }
    ),
  })
);
export const IdentifiersField = ({
  fieldPath,
  helpText,
  options,
  label,
  identifierLabel,
  className,
  identifierTypePlaceholder,
  identifierPlaceholder,
  defaultNewValue,
  validateOnBlur,
  ...uiProps
}) => {
  const { setFieldTouched, values } = useFormikContext();
  const identifiers = getIn(values, fieldPath, []);
  const handleValidateAndBlur = useValidateOnBlur();

  return (
    <ArrayField
      addButtonLabel={i18next.t("Add identifier")}
      fieldPath={fieldPath}
      label={label}
      labelIcon="pencil"
      helpText={helpText}
      className={className}
      defaultNewValue={defaultNewValue}
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <ArrayFieldItem
            indexPath={indexPath}
            arrayHelpers={arrayHelpers}
            fieldPathPrefix={fieldPathPrefix}
          >
            <SelectField
              clearable
              width={4}
              fieldPath={`${fieldPathPrefix}.scheme`}
              label={i18next.t("Identifier type")}
              required
              options={options.filter(
                (o) =>
                  !identifiers.map((i) => i.scheme).includes(o.value) ||
                  o.value === getIn(values, `${fieldPathPrefix}.scheme`)
              )}
              onBlur={
                validateOnBlur
                  ? () => handleValidateAndBlur(`${fieldPathPrefix}.scheme`)
                  : () => setFieldTouched(`${fieldPathPrefix}.scheme`)
              }
              placeholder={identifierTypePlaceholder}
              {...uiProps}
            />
            <TextField
              required
              width={12}
              fieldPath={`${fieldPathPrefix}.identifier`}
              placeholder={identifierPlaceholder}
              label={identifierLabel}
              onBlur={
                validateOnBlur
                  ? () => handleValidateAndBlur(`${fieldPathPrefix}.identifier`)
                  : () => setFieldTouched(`${fieldPathPrefix}.identifier`)
              }
            />
          </ArrayFieldItem>
        );
      }}
    </ArrayField>
  );
};

IdentifiersField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
  options: PropTypes.array.isRequired,
  label: PropTypes.string,
  identifierLabel: PropTypes.string,
  className: PropTypes.string,
  identifierTypePlaceholder: PropTypes.string,
  identifierPlaceholder: PropTypes.string,
  defaultNewValue: PropTypes.object,
  validateOnBlur: PropTypes.bool,
};

IdentifiersField.defaultProps = {
  label: i18next.t("Identifier field"),
  identifierLabel: i18next.t("Identifier"),
  identifierTypePlaceholder: i18next.t("e.g. ORCID, ISNI or ScopusID."),
  identifierPlaceholder: i18next.t("e.g. 10.1086/679716 for a DOI"),
  defaultNewValue: { scheme: "", identifier: "" },
  validateOnBlur: false,
};
