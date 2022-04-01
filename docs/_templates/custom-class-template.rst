{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:                                    <-- add at least this line
   :inherited-members:                          <-- ...and inherited members too
   :exclude-members: annual_mass_balance, ela, history, state_history, mb_gradient, response_time, specific_mass_balance ela, history, mb_gradient, response_time, specific_mass_balance, temp_bias, normal_years,
     surging_years

   {% block methods %}
   .. automethod:: __init__

   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
      :nosignatures:
   {% for item in methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

