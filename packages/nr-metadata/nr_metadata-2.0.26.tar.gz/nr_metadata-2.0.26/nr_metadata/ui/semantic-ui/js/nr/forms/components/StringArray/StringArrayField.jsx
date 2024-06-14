import React from "react";
import PropTypes from "prop-types";
import { FieldLabel, TextField } from "react-invenio-forms";
import { i18next } from "@translations/nr/i18next";
import { useFormikContext, getIn, FieldArray } from "formik";
import { Icon, Form } from "semantic-ui-react";
import {
  ArrayFieldItem,
  useShowEmptyValue,
  sanitizeInput,
} from "@js/oarepo_ui";

export const StringArrayField = ({
  fieldPath,
  label,
  required,
  defaultNewValue,
  addButtonLabel,
  helpText,
  labelIcon,
  showEmptyValue,
  validTags,
  ...uiProps
}) => {
  const { values, setFieldValue, setFieldTouched } = useFormikContext();
  useShowEmptyValue(fieldPath, defaultNewValue, showEmptyValue);

  return (
    <Form.Field>
      <FieldLabel label={label} icon={labelIcon} htmlFor={fieldPath} />
      <FieldArray
        name={fieldPath}
        render={(arrayHelpers) => (
          <React.Fragment>
            {getIn(values, fieldPath, []).map((item, index) => {
              const indexPath = `${fieldPath}.${index}`;
              return (
                <ArrayFieldItem
                  key={index}
                  indexPath={index}
                  arrayHelpers={arrayHelpers}
                  fieldPathPrefix={indexPath}
                >
                  <TextField
                    width={16}
                    fieldPath={indexPath}
                    label={`#${index + 1}`}
                    optimized
                    fluid
                    onBlur={() => {
                      const cleanedContent = sanitizeInput(
                        getIn(values, indexPath),
                        validTags
                      );
                      setFieldValue(indexPath, cleanedContent);
                      setFieldTouched(indexPath, true);
                    }}
                    {...uiProps}
                  />
                </ArrayFieldItem>
              );
            })}
            <label className="helptext">{helpText}</label>
            <Form.Button
              type="button"
              icon
              labelPosition="left"
              onClick={() => {
                arrayHelpers.push(defaultNewValue);
              }}
            >
              <Icon name="add" />
              {addButtonLabel}
            </Form.Button>
          </React.Fragment>
        )}
      />
    </Form.Field>
  );
};

StringArrayField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  defaultNewValue: PropTypes.string,
  addButtonLabel: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  helpText: PropTypes.string,
  labelIcon: PropTypes.string,
  required: PropTypes.bool,
  showEmptyValue: PropTypes.bool,
  validTags: PropTypes.array,
};

StringArrayField.defaultProps = {
  addButtonLabel: i18next.t("Add note"),
  defaultNewValue: "",
  labelIcon: "pencil",
  label: i18next.t("Notes"),
  helpText: i18next.t("Items shall be unique"),
  showEmptyValue: false,
};
